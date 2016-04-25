package gopipe

import (
	"time"
)

type DispPatcherCaller struct {
	dis       Dispatcher
	col       Collector
	ackr      Acker
	nanodelay int64
	ticker    *time.Ticker
}

func (dcaller *DispPatcherCaller) NewDispatcher(d Dispatcher, coll Collector,
	acker Acker, nanodelay int64) *DispPatcherCaller {
	if nanodelay < 0 {
		nanodelay = -nanodelay
	}
	ticker := time.NewTicker(time.Nanosecond * time.Duration(nanodelay))
	return &DispPatcherCaller{d, coll, acker, nanodelay, ticker}
}

func (dcaller *DispPatcherCaller) Stop() {
	dcaller.ticker.Stop()
}

func (dcaller *DispPatcherCaller) runCaller() {
	dcaller.dis.Prepare(dcaller.col, nil)
	for _ = range dcaller.ticker.C {
		dcaller.dis.LookForWork()
	}
	dcaller.dis.Shutdown()
}
