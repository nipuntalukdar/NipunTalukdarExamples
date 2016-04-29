package gopipe

import (
	"fmt"
	"testing"
	"time"
)

type Executor1 struct {
	col      Collector
	identity uint
}

func (ex *Executor1) Execute(input map[string]interface{}, context interface{}) {
	LOG.Infof("Executor1:%d emitting %v", ex.identity, input)
	input["data"] = "hello from one"
	ex.col.Emit(input, context)
	ex.col.Ack(context)
}

func (ex *Executor1) AddCollector(col Collector) {
	ex.col = col
}

func (ex *Executor1) AddIdentity(identity uint) {
	ex.identity = identity
}

type Executor2 struct {
	col      Collector
	identity uint
}

func (ex *Executor2) Execute(input map[string]interface{}, context interface{}) {
	LOG.Infof("Executor2:%d working on %v", ex.identity, input)
	mp := make(map[string]interface{})
	mp["data"] = input["data"].(string) + " two"
	ex.col.Emit(mp, context)
	ex.col.Ack(context)
}

func (ex *Executor2) AddCollector(col Collector) {
	ex.col = col
}

func (ex *Executor2) AddIdentity(identity uint) {
	ex.identity = identity
}

type Executor3 struct {
	col      Collector
	identity uint
}

func (ex *Executor3) Execute(input map[string]interface{}, context interface{}) {
	LOG.Infof("Executor3:%d working on %v", ex.identity, input)
	mp := make(map[string]interface{})
	mp["data"] = input["data"].(string) + " three"
	ex.col.Emit(mp, context)
	ex.col.Ack(context)
}

func (ex *Executor3) AddCollector(col Collector) {
	ex.col = col
}

func (ex *Executor3) AddIdentity(identity uint) {
	ex.identity = identity
}

type Executor4 struct {
	col      Collector
	identity uint
}

func (ex *Executor4) Execute(input map[string]interface{}, context interface{}) {
	LOG.Infof("Executor4:%d working on %v", ex.identity, input)
	ex.col.Ack(context)
}

func (ex *Executor4) AddCollector(col Collector) {
	ex.col = col
}

func (ex *Executor4) AddIdentity(identity uint) {
	ex.identity = identity
}

type DispatcherEx struct {
	tr  *Tracker
	col Collector
}

func (disp *DispatcherEx) LookForWork() {
	mp := make(map[string]interface{})
	mp[NewRandomUUIDStr()] = NewRandomUUIDStr()
	LOG.Infof("Looking for work")
	disp.col.Emit(mp, NewRandomUUIDStr())
}

func (disp *DispatcherEx) Fail(id string) {
	LOG.Infof("Failed msg id %s", id)
}

func (disp *DispatcherEx) Ack(id string) {
	LOG.Infof("Processed msg id %s", id)
}

func (disp *DispatcherEx) TimedOut(id string) {
	LOG.Infof("Timing out %s\n", id)
}

func (disp *DispatcherEx) Prepare(col Collector, tr *Tracker) {
	disp.tr = tr
	disp.col = col
}

func (disp *DispatcherEx) Shutdown() {
	fmt.Println("Shutting down")
}

func TestExecutionTree(t *testing.T) {

	LOG.Infof("Starting tree.... \n")
	exreg := GetRegistry()
	dispreg := GetDispRegistry()
	dispreg.AddType("dispatcher1", new(DispatcherEx))
	exreg.AddType("executor1", new(Executor1))
	exreg.AddType("executor2", new(Executor2))
	exreg.AddType("executor3", new(Executor3))
	exreg.AddType("executor4", new(Executor4))

	dispstgInfo_one := NewDispatcherStageInfo(10, "dispatcher1", "disp1")
	stageInfo_one := NewStageInfo(10, "executor1", "first")
	stageInfo_two := NewStageInfo(10, "executor2", "second")
	stageInfo_three := NewStageInfo(10, "executor3", "third")
	stageInfo_four := NewStageInfo(40, "executor4", "fourth")
	stageInfo_one.AddStage(stageInfo_two, false)
	stageInfo_one.AddStage(stageInfo_four, false)
	stageInfo_two.AddStage(stageInfo_three, false)
	stageInfo_two.AddStage(stageInfo_four, false)
	stageInfo_three.AddStage(stageInfo_four, false)
	dispstgInfo_one.AddOutStage(stageInfo_one)

	All.Print()
	CreateExecutionTree()
	Run()
	t.Logf("Started ...")
	time.Sleep(1000000 * time.Second)
}
