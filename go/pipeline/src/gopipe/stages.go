package gopipe

import (
	"fmt"
	"time"
)

type StageInfo struct {
	input_stages   []*StageInfo
	executor_class string
	num_tasks      int
	name           string
	output_stages  []*StageInfo
}

type DispatcherStageInfo struct {
	output_stages    []*StageInfo
	dispatcher_class string
	num_tasks        int
	name             string
}

type AllStages struct {
	dispstages map[string]*DispatcherStageInfo
	stages     map[string]*StageInfo
	stagechans map[string]chan map[string]interface{}
}

var All *AllStages

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
	for _, sexisting := range dsinfo.output_stages {
		if sexisting == s {
			return
		}
	}
	dsinfo.output_stages = append(dsinfo.output_stages, s)
}

func (sinfo *StageInfo) AddStage(s *StageInfo, isinput bool) {
	var x []*StageInfo
	All.addStage(s)
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
	input_chan chan map[string]interface{}
	exc        Executor
	col        Collector
}

var callers []*ExecutorCaller
var dispcallers []*DispPatcherCaller
var i int

func init() {
	callers = make([]*ExecutorCaller, 0)
	dispcallers = make([]*DispPatcherCaller, 0)
	i = 0
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
	stagechans := make(map[string]chan map[string]interface{})
	for name, _ := range All.stages {
		stagechans[name] = make(chan map[string]interface{}, 10240)
	}

	All.stagechans = stagechans
	var tc *TupleCollector
	i := 0
	for _, stage := range All.stages {
		tc = nil
		for i = 0; i < stage.num_tasks; i++ {
			ex_caller := new(ExecutorCaller)
			exc := exreg.GetInstance(stage.executor_class)
			ex_caller.exc = exc
			ex_caller.input_chan = stagechans[stage.name]
			callers = append(callers, ex_caller)
			if len(stage.output_stages) == 0 {
				continue
			}
			if tc == nil {
				tc = NewTupleCollector(stage.name)
				for _, stg := range stage.output_stages {
					tc.AddOutput(stagechans[stg.name])
				}
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
			disp_caller.ticker = time.NewTicker(time.Nanosecond * 10000000)
			dispcallers = append(dispcallers, disp_caller)
			if len(dispstage.output_stages) == 0 {
				continue
			}
			if tc == nil {
				tc = NewTupleCollector(dispstage.name)
				for _, stg := range dispstage.output_stages {
					tc.AddOutput(stagechans[stg.name])
				}
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

func (All *AllStages) getChan(stage string) chan map[string]interface{} {
	ch, ok := All.stagechans[stage]
	if ok {
		return ch
	}
	return nil
}

func init() {
	All = newAllStageInfo()
}

func taskRunner(caller *ExecutorCaller, i int) {
	caller.exc.AddIdentity(i)
	for {
		data := <-caller.input_chan
		caller.exc.Execute(data)
	}
}

func Run() {
	i := 1
	for _, caller := range callers {
		go taskRunner(caller, i)
		i++
	}

	for _, dispcaller := range dispcallers {
		go func() {
			dispcaller.runCaller()
		}()
	}
}
