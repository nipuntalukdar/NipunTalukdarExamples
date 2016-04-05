package main

import (
	"fmt"
	"gopipe"
	//	"time"
)

type Executor1 struct {
	col gopipe.Collector
}

func (ex Executor1) Execute(input map[string]interface{}) {
	fmt.Printf("Executor1 %v\n", input)
	input["fromone"] = "hello"
	ex.col.Emit(input)
}

func (ex Executor1) AddCollector(col gopipe.Collector) {
	ex.col = col
}

type Executor2 struct {
	col gopipe.Collector
}

func (ex Executor2) Execute(input map[string]interface{}) {
	fmt.Printf("Executor2 %v\n", input)
	input["from2"] = "hi"
}

func (ex Executor2) AddCollector(col gopipe.Collector) {
	ex.col = col
}

func main() {

	exreg := gopipe.GetRegistry()
	exreg.AddType("executor1", Executor1{})
	exreg.AddType("executor2", Executor2{})

	x := exreg.GetInstance("executor1")
	mp := make(map[string]interface{})
	y := *x
	y.Execute(mp)
	/*

		stageInfo_one := gopipe.NewStageInfo(1, "executor1", "first")
		stageInfo_two := gopipe.NewStageInfo(1, "executor2", "second")
		stageInfo_one.AddStage(stageInfo_two, false)
		stageInfo_two.AddStage(stageInfo_one, true)
		ch := make(chan map[string]interface{})
		gopipe.CreateExecutionTree(stageInfo_one, ch)
		gopipe.Run()
		mp := make(map[string]interface{})
		i := 1
		mp["one"] = i
		for {
			time.Sleep(1 * time.Second)
			ch <- mp
			i++
			mp["one"] = i
		}
	*/
}
