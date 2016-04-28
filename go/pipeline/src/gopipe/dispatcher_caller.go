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
	id        uint
}

func (dcaller *DispPatcherCaller) NewDispatcher(d Dispatcher, coll Collector,
	acker Acker, nanodelay int64, id uint) *DispPatcherCaller {
	if nanodelay < 0 {
		nanodelay = -nanodelay
	}
	ticker := time.NewTicker(time.Nanosecond * time.Duration(nanodelay))
	GetAcker().AddTracker(id, d)
	return &DispPatcherCaller{d, coll, acker, nanodelay, ticker, id}
}

func (dcaller *DispPatcherCaller) Stop() {
	dcaller.ticker.Stop()
}

func (dcaller *DispPatcherCaller) runCaller() {
	dcaller.dis.Prepare(dcaller.col, nil)
	GetAcker().AddTracker(dcaller.id, dcaller.dis)
	for _ = range dcaller.ticker.C {
		dcaller.dis.LookForWork()
	}
	dcaller.dis.Shutdown()
}
