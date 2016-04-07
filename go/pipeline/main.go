package main

import (
	"fmt"
	"gopipe"
)

type Executor1 struct {
	col      gopipe.Collector
	identity int
}

func (ex *Executor1) Execute(input map[string]interface{}) {
	gopipe.Log(fmt.Sprintf("Executor1:%d emitting %v\n", ex.identity, input))
	input["fromone"] = "hello"
	ex.col.Emit(input)
}

func (ex *Executor1) AddCollector(col gopipe.Collector) {
	ex.col = col
}

func (ex *Executor1) AddIdentity(identity int) {
	ex.identity = identity
}

type Executor2 struct {
	col      gopipe.Collector
	identity int
}

func (ex *Executor2) Execute(input map[string]interface{}) {
	gopipe.Log(fmt.Sprintf("Executor2:%d working on %v\n", ex.identity, input))
}

func (ex *Executor2) AddCollector(col gopipe.Collector) {
	ex.col = col
}

func (ex *Executor2) AddIdentity(identity int) {
	ex.identity = identity
}

func main() {

	exreg := gopipe.GetRegistry()
	exreg.AddType("executor1", new(Executor1))
	exreg.AddType("executor2", new(Executor2))

	stageInfo_one := gopipe.NewStageInfo(10000, "executor1", "first")
	stageInfo_two := gopipe.NewStageInfo(10000, "executor2", "second")
	stageInfo_one.AddStage(stageInfo_two, false)
	stageInfo_two.AddStage(stageInfo_one, true)
	ch := make(chan map[string]interface{})
	gopipe.CreateExecutionTree(stageInfo_one, ch)
	gopipe.Run()
	gopipe.Log(fmt.Sprintf("Started ..."))
	mp := make(map[string]interface{})
	i := 1
	mp["one"] = i
	for {
		ch <- mp
		i++
		mp = make(map[string]interface{})
		mp["one"] = i
	}
}
