package gopipe

import (
	"fmt"
	"time"
)

type outGroupStages struct {
	name         string
	groupingKeys []string
}

type StageInfo struct {
	input_stages         []*StageInfo
	grpd_inp_stages      []*StageInfo
	grpd_inp_disp_stages []*DispatcherStageInfo
	executor_class       string
	num_tasks            int
	name                 string
	output_stages        []*StageInfo
	grpd_out_stages      map[string]outGroupStages
	numOutGroup          int
}

type DispatcherStageInfo struct {
	output_stages    []*StageInfo
	grpd_out_stages  map[string]outGroupStages
	numOutGroup      int
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
	x.grpd_out_stages = make(map[string]outGroupStages)
	return x
}

func NewDispatcherStageInfo(num_tasks int, dispatcher_class string, name string) *DispatcherStageInfo {
	x := new(DispatcherStageInfo)
	x.dispatcher_class = dispatcher_class
	x.num_tasks = num_tasks
	x.name = name
	x.grpd_out_stages = make(map[string]outGroupStages)
	return x
}

func (sinfo *DispatcherStageInfo) CheckStage(s *StageInfo) {
	for _, outstage := range sinfo.output_stages {
		if outstage.name == s.name {
			for name, _ := range sinfo.grpd_out_stages {
				if name == s.name {
					panic(fmt.Sprintf("Stage:%s in both grouping/non-grouping stage to :%s",
						s.name, sinfo.name))
					break
				}
			}
			break
		}
	}
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
	dsinfo.CheckStage(s)
}

func (dsinfo *DispatcherStageInfo) AddGroupingOutStage(s *StageInfo, groupField []string) {
	if len(groupField) == 0 {
		panic("invalid grouping keys")
	}
	_, ok := dsinfo.grpd_out_stages[s.name]
	if ok {
		return
	}
	outgroup := outGroupStages{s.name, []string{}}
	for _, key := range groupField {
		if isInArray(key, outgroup.groupingKeys) {
			continue
		}
		outgroup.groupingKeys = append(outgroup.groupingKeys, key)
	}
	dsinfo.grpd_out_stages[s.name] = outgroup
	dsinfo.numOutGroup++
	All.addDispStage(dsinfo)
	All.addStage(s)
	s.AddDispGroupingStage(dsinfo)
	dsinfo.CheckStage(s)
}

func (sinfo *StageInfo) AddGroupingStage(s *StageInfo, groupFields []string, isinput bool) {
	if isinput && isInStages(sinfo.grpd_inp_stages, s) {
		return
	}
	if !isinput {
		_, ok := sinfo.grpd_out_stages[s.name]
		if !ok {
			outgroup := outGroupStages{s.name, []string{}}
			for _, key := range groupFields {
				if isInArray(key, outgroup.groupingKeys) {
					continue
				}
				outgroup.groupingKeys = append(outgroup.groupingKeys, key)
			}
			sinfo.grpd_out_stages[s.name] = outgroup
			s.AddGroupingStage(sinfo, groupFields, !isinput)
			sinfo.numOutGroup++
		}
	} else {
		if !isInStages(sinfo.grpd_inp_stages, s) {
			sinfo.grpd_inp_stages = append(sinfo.grpd_inp_stages, s)
			s.AddGroupingStage(sinfo, groupFields, !isinput)
		}
	}
	All.addStage(sinfo)
	All.addStage(s)
	sinfo.CheckStage(s, isinput)
}

func (sinfo *StageInfo) AddDispGroupingStage(disp *DispatcherStageInfo) {
	if isInDispStages(sinfo.grpd_inp_disp_stages, disp) {
		return
	}
	sinfo.grpd_inp_disp_stages = append(sinfo.grpd_inp_disp_stages, disp)
	All.addDispStage(disp)
}

func (sinfo *StageInfo) CheckStage(s *StageInfo, isinput bool) {
	if isinput {
		for _, inpstage := range sinfo.input_stages {
			if inpstage.name == s.name {
				for _, inpgrpstage := range sinfo.grpd_inp_stages {
					if inpgrpstage.name == s.name {
						panic(fmt.Sprintf("Stage:%s in both grouping/non-grouping stage to :%s",
							s.name, sinfo.name))
						break
					}
				}
				break
			}
		}
	} else {
		for _, outstage := range sinfo.output_stages {
			if outstage.name == s.name {
				for name, _ := range sinfo.grpd_out_stages {
					if name == s.name {
						panic(fmt.Sprintf("Stage:%s in both grouping/non-grouping stage to :%s",
							s.name, sinfo.name))
						break
					}
				}
				break
			}
		}
	}
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
	// Don't allow the same stage as grouping or non-grouping stage
	sinfo.CheckStage(s, isinput)
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
		for _, instage := range stage.grpd_inp_stages {
			node.AddInNode(npl.Get(instage.name))
		}
		for _, outstage := range stage.output_stages {
			node.AddOutNode(npl.Get(outstage.name))
		}
		for name, _ := range stage.grpd_out_stages {
			node.AddOutNode(npl.Get(name))
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
		for i = 0; i < stage.num_tasks; i++ {
			ex_caller := new(ExecutorCaller)
			exc := exreg.GetInstance(stage.executor_class)
			ex_caller.exc = exc
			ex_caller.input_chan = stagechans[stage.name]
			ex_caller.id = nextids.NextId()
			_, ok := grouped_chans[name]
			if ok {
				ex_caller.grp_chan = grouped_chans[name][i]
			}
			callers = append(callers, ex_caller)
			if tc == nil {
				tc = NewTupleCollector(stage.name, nextids.NextId(), 0)
				for _, stg := range stage.output_stages {
					tc.AddOutput(stagechans[stg.name])
				}
				for stagename, outGroup := range stage.grpd_out_stages {
					chans := grouped_chans[stagename]
					tc.groupd_chans = append(tc.groupd_chans, &groupedChans{stagename,
						outGroup.groupingKeys, uint32(len(chans)), chans})
					tc.groupd_chans[len(tc.groupd_chans)-1].groupKeys = copyStringSlice(outGroup.groupingKeys)
					for _, key := range outGroup.groupingKeys {
						addIfNotPresent(key, &tc.all_group_keys)
					}
					tc.num_grouped++
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
			if len(dispstage.output_stages) == 0 && len(dispstage.grpd_out_stages) == 0 {
				continue
			}
			if tc == nil {
				tc = NewTupleCollector(dispstage.name, disp_caller.id, disp_caller.id)
				for _, stg := range dispstage.output_stages {
					tc.AddOutput(stagechans[stg.name])
				}
				for stagename, outGroup := range dispstage.grpd_out_stages {
					chans := grouped_chans[stagename]
					tc.groupd_chans = append(tc.groupd_chans, &groupedChans{stagename,
						outGroup.groupingKeys, uint32(len(chans)), chans})
					tc.groupd_chans[len(tc.groupd_chans)-1].groupKeys = copyStringSlice(outGroup.groupingKeys)
					for _, key := range outGroup.groupingKeys {
						addIfNotPresent(key, &tc.all_group_keys)
					}
					tc.num_grouped++
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
