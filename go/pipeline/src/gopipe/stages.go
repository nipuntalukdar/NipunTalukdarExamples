package gopipe

import (
	"fmt"
	"time"
)

type StageInfo struct {
	input_stages         []*StageInfo
	grpd_inp_stages      []*StageInfo
	grpd_inp_disp_stages []*DispatcherStageInfo
	executor_class       string
	num_tasks            int
	name                 string
	output_stages        []*StageInfo
	grpd_out_stages      map[string][]*StageInfo
}

type DispatcherStageInfo struct {
	output_stages    []*StageInfo
	grpd_out_stages  map[string][]*StageInfo
	dispatcher_class string
	num_tasks        int
	name             string
}

type OutPut struct {
	data    map[string]interface{}
	context interface{}
}

type AllStages struct {
	dispstages map[string]*DispatcherStageInfo
	stages     map[string]*StageInfo
	stagechans map[string]chan *OutPut
}

var All *AllStages

func isInStages(inp []*StageInfo, st *StageInfo) bool {
	for _, s := range inp {
		if s == st {
			return true
		}
	}
	return false
}

func isInDispStages(inp []*DispatcherStageInfo, st *DispatcherStageInfo) bool {
	for _, s := range inp {
		if s == st {
			return true
		}
	}
	return false
}

func NewStageInfo(num_tasks int, executor_class string, name string) *StageInfo {
	x := new(StageInfo)
	x.executor_class = executor_class
	x.num_tasks = num_tasks
	x.name = name
	return x
}

func NewDispatcherStageInfo(num_tasks int, dispatcher_class string, name string) *DispatcherStageInfo {
	x := new(DispatcherStageInfo)
	x.dispatcher_class = dispatcher_class
	x.num_tasks = num_tasks
	x.name = name
	return x
}

func (dsinfo *DispatcherStageInfo) AddOutStage(s *StageInfo) {
	All.addDispStage(dsinfo)
	All.addStage(s)
	for _, sexisting := range dsinfo.output_stages {
		if sexisting == s {
			return
		}
	}
	dsinfo.output_stages = append(dsinfo.output_stages, s)
}

func (dsinfo *DispatcherStageInfo) AddGroupingOutStage(s *StageInfo, groupField string) {
	stages, ok := dsinfo.grpd_out_stages[groupField]
	if ok {
		if isInStages(stages, s) {
			return
		}
		stages = []*StageInfo{}
	}
	dsinfo.grpd_out_stages[groupField] = append(stages, s)
	All.addDispStage(dsinfo)
	All.addStage(s)
	s.AddDispGroupingStage(dsinfo)
}

func (sinfo *StageInfo) AddGroupingStage(s *StageInfo, groupField string, isinput bool) {
	if isinput && isInStages(sinfo.grpd_inp_stages, s) {
		return
	}
	if !isinput {
		stages, ok := sinfo.grpd_out_stages[groupField]
		if ok {
			if isInStages(stages, s) {
				return
			}
		} else {
			stages = []*StageInfo{}
		}
		sinfo.grpd_out_stages[groupField] = append(stages, s)
		s.AddGroupingStage(sinfo, groupField, true)
	} else {
		sinfo.grpd_inp_stages = append(sinfo.grpd_inp_stages, s)
		s.AddGroupingStage(sinfo, groupField, false)
	}
	All.addStage(s)
	All.addStage(sinfo)
}

func (sinfo *StageInfo) AddDispGroupingStage(disp *DispatcherStageInfo) {
	if isInDispStages(sinfo.grpd_inp_disp_stages, disp) {
		return
	}
	sinfo.grpd_inp_disp_stages = append(sinfo.grpd_inp_disp_stages, disp)
	All.addDispStage(disp)
}

func (sinfo *StageInfo) AddStage(s *StageInfo, isinput bool) {
	var x []*StageInfo
	All.addStage(s)
	All.addStage(sinfo)
	if isinput {
		x = sinfo.input_stages
	} else {
		x = sinfo.output_stages
	}
	for _, sexisting := range x {
		if sexisting == s {
			return
		}
	}
	x = append(x, s)
	if isinput {
		sinfo.input_stages = x
	} else {
		sinfo.output_stages = x
	}
	s.AddStage(sinfo, !isinput)
}

type ExecutorCaller struct {
	input_chan chan *OutPut
	grp_chan   chan *OutPut
	exc        Executor
	col        Collector
	id         uint
}

var callers []*ExecutorCaller
var dispcallers []*DispPatcherCaller
var i int
var nextids *NextIdGetter

func init() {
	callers = make([]*ExecutorCaller, 0)
	dispcallers = make([]*DispPatcherCaller, 0)
	i = 0
	nextids = NewNextIdGettr(1)
}

func getExecutionGraph(allstgs *AllStages) *GraphNodePool {
	npl := GetNewGraphNodePool()
	for name, stage := range allstgs.stages {
		node := npl.Get(name)
		for _, instage := range stage.input_stages {
			node.AddInNode(npl.Get(instage.name))
		}
		for _, outstage := range stage.output_stages {
			node.AddOutNode(npl.Get(outstage.name))
		}
	}

	return npl
}

func CreateExecutionTree() {
	npl := getExecutionGraph(All)
	if npl.DetectAnyCycle() {
		panic("Dectected cycle in execution tree, exiting")
	}
	exreg := GetRegistry()
	stagechans := make(map[string]chan *OutPut)
	grouped_chans := make(map[string][]chan *OutPut)
	for name, stg := range All.stages {
		stagechans[name] = make(chan *OutPut, 10240)
		if len(stg.grpd_inp_stages) > 0 || len(stg.grpd_inp_disp_stages) > 0 {
			group_chans := []chan *OutPut{}
			for i := 0; i < stg.num_tasks; i++ {
				group_chans = append(group_chans, make(chan *OutPut, 10240))
			}
			grouped_chans[name] = group_chans
		}
	}

	All.stagechans = stagechans
	var tc *TupleCollector
	i := 0
	for name, stage := range All.stages {
		tc = nil
		group_chans, grouped := grouped_chans[name]
		for i = 0; i < stage.num_tasks; i++ {
			ex_caller := new(ExecutorCaller)
			exc := exreg.GetInstance(stage.executor_class)
			ex_caller.exc = exc
			ex_caller.input_chan = stagechans[stage.name]
			if grouped {
				ex_caller.grp_chan = group_chans[i]
			}
			ex_caller.id = nextids.NextId()
			callers = append(callers, ex_caller)
			if tc == nil {
				tc = NewTupleCollector(stage.name, nextids.NextId(), 0)
				for _, stg := range stage.output_stages {
					tc.AddOutput(stagechans[stg.name])
				}
			} else {
				tc = tc.Copy()
				tc.id = uint64(ex_caller.id) << 32
			}
			ex_caller.col = tc
			ex_caller.exc.AddCollector(tc)
		}
	}
	for _, dispstage := range All.dispstages {
		tc = nil
		for i = 0; i < dispstage.num_tasks; i++ {
			disp_caller := new(DispPatcherCaller)
			disp := dispreg.GetInstance(dispstage.dispatcher_class)
			disp_caller.dis = disp
			disp_caller.id = nextids.NextId()
			disp_caller.ticker = time.NewTicker(time.Millisecond * 10)
			dispcallers = append(dispcallers, disp_caller)
			if len(dispstage.output_stages) == 0 {
				continue
			}
			if tc == nil {
				tc = NewTupleCollector(dispstage.name, disp_caller.id, disp_caller.id)
				for _, stg := range dispstage.output_stages {
					tc.AddOutput(stagechans[stg.name])
				}
			} else {
				tc = tc.Copy()
				tc.id = uint64(disp_caller.id) << 32
				tc.isdisp = disp_caller.id
			}
			disp_caller.col = tc
		}
	}
}

func newAllStageInfo() *AllStages {
	ret := new(AllStages)
	ret.stages = make(map[string]*StageInfo)
	ret.dispstages = make(map[string]*DispatcherStageInfo)
	return ret
}

func (All *AllStages) addStage(stg *StageInfo) {
	All.stages[stg.name] = stg
}

func (All *AllStages) addDispStage(stg *DispatcherStageInfo) {
	All.dispstages[stg.name] = stg
}

func (All *AllStages) Print() {
	for name, stge := range All.stages {
		fmt.Printf("%v %v\n", name, stge)
	}
}

func (All *AllStages) getChan(stage string) chan *OutPut {
	ch, ok := All.stagechans[stage]
	if ok {
		return ch
	}
	return nil
}

func init() {
	All = newAllStageInfo()
}

func taskRunner(caller *ExecutorCaller) {
	caller.exc.AddIdentity(caller.id)
	if caller.grp_chan == nil {
		for {
			data := <-caller.input_chan
			caller.exc.Execute(data.data, data.context)
		}
	} else {
		var data *OutPut
		for {
			select {
			case data = <-caller.input_chan:
			case data = <-caller.grp_chan:
			}
			caller.exc.Execute(data.data, data.context)
		}
	}
}

func Run() {
	for _, caller := range callers {
		go taskRunner(caller)
	}

	for _, dispcaller := range dispcallers {
		GetAcker().AddTracker(dispcaller.id, dispcaller.dis)
	}

	for _, dispcaller := range dispcallers {
		go func(disp_caller *DispPatcherCaller) {
			disp_caller.runCaller()
		}(dispcaller)
	}
}
