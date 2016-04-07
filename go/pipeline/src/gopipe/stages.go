package gopipe

import (
	"fmt"
)

type Stage struct {
	input_chan   chan map[string]interface{}
	output_chans []chan map[string]interface{}
}

func (stg *Stage) chanPresent(input bool, ch chan map[string]interface{}) bool {
	if input {
		return stg.input_chan == ch
	}
	for _, och := range stg.output_chans {
		if och == ch {
			return true
		}
	}
	return false
}

func (stage *Stage) AddChan(isinput bool, chn chan map[string]interface{}) {
	if !stage.chanPresent(isinput, chn) {
		if isinput {
			stage.input_chan = chn
		} else {
			stage.output_chans = append(stage.output_chans, chn)
		}
	}
}

type StageInfo struct {
	input_stages   []*StageInfo
	executor_class string
	num_tasks      int
	name           string
	output_statges []*StageInfo
}

func NewStageInfo(num_tasks int, executor_class string, name string) *StageInfo {
	x := new(StageInfo)
	x.executor_class = executor_class
	x.num_tasks = num_tasks
	return x
}

func (sinfo *StageInfo) AddStage(s *StageInfo, isinput bool) {
	var x []*StageInfo
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
}

type ExecutorCaller struct {
	input_chan chan map[string]interface{}
	exc        Executor
	col        Collector
}

var callers []*ExecutorCaller

func init() {
	callers = []*ExecutorCaller{}
}

func CreateExecutionTree(stageInfo *StageInfo, input_chan chan map[string]interface{}) {
	if stageInfo == nil {
		return
	}
	exreg := GetRegistry()
	tc := NewTupleCollector(stageInfo.name)
	for num_tasks := stageInfo.num_tasks; num_tasks > 0; num_tasks-- {
		ex_caller := new(ExecutorCaller)
		exc := exreg.GetInstance(stageInfo.executor_class)
		ex_caller.exc = exc
		ex_caller.input_chan = input_chan
		callers = append(callers, ex_caller)
		if len(stageInfo.output_statges) == 0 {
			continue
		}
		ex_caller.col = tc
		ex_caller.exc.AddCollector(tc)
	}
	for _, stage := range stageInfo.output_statges {
		ch_out := make(chan map[string]interface{})
		tc.AddOutput(ch_out)
		CreateExecutionTree(stage, ch_out)
	}
}

func taskRunner(caller *ExecutorCaller) {
	if caller.col != nil {
		fmt.Printf("Collector %v\n", caller.col)
	}
	for {
		data := <-caller.input_chan
		caller.exc.Execute(data)
	}
}

func Run() {
	for _, caller := range callers {
		go taskRunner(caller)
	}
}
