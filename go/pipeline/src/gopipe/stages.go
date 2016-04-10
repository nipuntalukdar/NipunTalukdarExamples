package gopipe

import (
	"fmt"
)

type StageInfo struct {
	input_stages   []*StageInfo
	executor_class string
	num_tasks      int
	name           string
	output_statges []*StageInfo
}

type AllStages struct {
	stages map[string]*StageInfo
	mp     map[string]chan map[string]interface{}
}

var All *AllStages

func NewStageInfo(num_tasks int, executor_class string, name string) *StageInfo {
	x := new(StageInfo)
	x.executor_class = executor_class
	x.num_tasks = num_tasks
	x.name = name
	return x
}

func (sinfo *StageInfo) AddStage(s *StageInfo, isinput bool) {
	var x []*StageInfo
	All.addStage(s)
	if isinput {
		x = sinfo.input_stages
	} else {
		x = sinfo.output_statges
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
		sinfo.output_statges = x
	}
	s.AddStage(sinfo, !isinput)
}

type ExecutorCaller struct {
	input_chan chan map[string]interface{}
	exc        Executor
	col        Collector
}

var callers []*ExecutorCaller
var i int

func init() {
	callers = []*ExecutorCaller{}
	i = 0
}

func getExecutionGraph(allstgs *AllStages) *GraphNodePool {
	npl := GetNewGraphNodePool()
	for name, stage := range allstgs.stages {
		node := npl.Get(name)
		for _, instage := range stage.input_stages {
			node.AddInNode(npl.Get(instage.name))
		}
		for _, outstage := range stage.output_statges {
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
	mp := make(map[string]chan map[string]interface{})
	for name, _ := range All.stages {
		mp[name] = make(chan map[string]interface{}, 10240)
	}

	All.mp = mp
	var tc *TupleCollector
	i := 0
	for _, stage := range All.stages {
		tc = nil
		for i = 0; i < stage.num_tasks; i++ {
			ex_caller := new(ExecutorCaller)
			exc := exreg.GetInstance(stage.executor_class)
			ex_caller.exc = exc
			ex_caller.input_chan = mp[stage.name]
			callers = append(callers, ex_caller)
			if len(stage.output_statges) == 0 {
				continue
			}
			if tc == nil {
				tc = NewTupleCollector(stage.name)
				for _, stg := range stage.output_statges {
					tc.AddOutput(mp[stg.name])
				}
			}
			ex_caller.col = tc
			ex_caller.exc.AddCollector(tc)
		}
	}
}

func newAllStageInfo() *AllStages {
	ret := new(AllStages)
	ret.stages = make(map[string]*StageInfo)
	return ret
}

func (All *AllStages) addStage(stg *StageInfo) {
	All.stages[stg.name] = stg
}

func (All *AllStages) Print() {
	for name, stge := range All.stages {
		fmt.Printf("%v %v\n", name, stge)
	}
}

func (All *AllStages) GetChan(stage string) chan map[string]interface{} {
	ch, ok := All.mp[stage]
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
}
