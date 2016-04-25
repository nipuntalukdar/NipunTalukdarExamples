package gopipe

type Dispatcher interface {
	LookForWork()
	Fail(string)
	Ack(string)
	TimedOut(string)
	Prepare(col Collector, tr *Tracker)
	Shutdown()
}
