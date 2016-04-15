package gopipe

type Dispatcher interface {
	LookForWork()
	Dispatch(map[string]interface{})
	Fail(string)
	Ack(string)
	TimedOut(string)
	AddHeadStage([]string)
	Prepare(col *Collector, tr *Tracker)
	Shutdown()
}
