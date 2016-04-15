package gopipe

import (
	"fmt"
	"testing"
	"time"
)

type Executor1 struct {
	col      Collector
	identity int
}

func (ex *Executor1) Execute(input map[string]interface{}) {
	LOG.Infof("Executor1:%d emitting %v", ex.identity, input)
	input["data"] = "hello from one"
	ex.col.Emit(input)
}

func (ex *Executor1) AddCollector(col Collector) {
	ex.col = col
}

func (ex *Executor1) AddIdentity(identity int) {
	ex.identity = identity
}

type Executor2 struct {
	col      Collector
	identity int
}

func (ex *Executor2) Execute(input map[string]interface{}) {
	LOG.Infof("Executor2:%d working on %v", ex.identity, input)
	mp := make(map[string]interface{})
	mp["data"] = input["data"].(string) + " two"
	ex.col.Emit(mp)
}

func (ex *Executor2) AddCollector(col Collector) {
	ex.col = col
}

func (ex *Executor2) AddIdentity(identity int) {
	ex.identity = identity
}

type Executor3 struct {
	col      Collector
	identity int
}

func (ex *Executor3) Execute(input map[string]interface{}) {
	LOG.Infof("Executor3:%d working on %v", ex.identity, input)
	mp := make(map[string]interface{})
	mp["data"] = input["data"].(string) + " three"
	ex.col.Emit(mp)
}

func (ex *Executor3) AddCollector(col Collector) {
	ex.col = col
}

func (ex *Executor3) AddIdentity(identity int) {
	ex.identity = identity
}

type Executor4 struct {
	col      Collector
	identity int
}

func (ex *Executor4) Execute(input map[string]interface{}) {
	LOG.Infof("Executor4:%d working on %v", ex.identity, input)
}

func (ex *Executor4) AddCollector(col Collector) {
	ex.col = col
}

func (ex *Executor4) AddIdentity(identity int) {
	ex.identity = identity
}

type DemoDispatcher struct {
	tr  *tracker
	col *Collector
}

func (dispatcher *DemoDispatcher) LookForWork {
	time.Sleep(1)
    	
}

func TestExecutionTree(t *testing.T) {

	fmt.Printf("Starting tree.... \n")
	exreg := GetRegistry()
	exreg.AddType("executor1", new(Executor1))
	exreg.AddType("executor2", new(Executor2))
	exreg.AddType("executor3", new(Executor3))
	exreg.AddType("executor4", new(Executor4))

	stageInfo_one := NewStageInfo(10, "executor1", "first")
	stageInfo_two := NewStageInfo(10, "executor2", "second")
	stageInfo_three := NewStageInfo(10, "executor3", "third")
	stageInfo_four := NewStageInfo(40, "executor4", "fourth")
	stageInfo_one.AddStage(stageInfo_two, false)
	stageInfo_one.AddStage(stageInfo_four, false)
	stageInfo_two.AddStage(stageInfo_three, false)
	stageInfo_two.AddStage(stageInfo_four, false)
	stageInfo_three.AddStage(stageInfo_four, false)

	All.Print()
	CreateExecutionTree()
	Run()
	t.Logf("Started ...")
	ch := All.GetChan("first")
	mp := make(map[string]interface{})
	i := 1
	mp["data"] = i
	for i < 1000000 {
		i++
		mp = make(map[string]interface{})
		mp["data"] = i
		ch <- mp
	}
}
