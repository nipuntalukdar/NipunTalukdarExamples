package gopipe

import (
	"time"
)

type DispPatcherCaller struct {
	dis         Dispatcher
	col         Collector
	ackr        Acker
	nanodelay   int64
	ticker      *time.Ticker
	id          uint
	max_unacked uint32
}

func (dcaller *DispPatcherCaller) NewDispatcher(d Dispatcher, coll Collector,
	acker Acker, nanodelay int64, id uint) *DispPatcherCaller {
	if nanodelay < 0 {
		nanodelay = -nanodelay
	}
	ticker := time.NewTicker(time.Nanosecond * time.Duration(nanodelay))
	return &DispPatcherCaller{d, coll, acker, nanodelay, ticker, id,
		GetConfig().GetMaxUnacked()}
}

func (dcaller *DispPatcherCaller) Stop() {
	dcaller.ticker.Stop()
}

func (dcaller *DispPatcherCaller) runCaller() {
	dcaller.dis.Prepare(dcaller.col, nil)
	max_unacked := int32(GetConfig().GetMaxUnacked())
	for _ = range dcaller.ticker.C {
		if dcaller.col.getEmittedTracked() >= max_unacked {
			LOG.Infof("MAX unacked id:%d unacked:%d", dcaller.id, dcaller.col.getEmittedTracked())
			continue
		}
		dcaller.dis.LookForWork()
	}
	dcaller.dis.Shutdown()
}

func (dcaller *DispPatcherCaller) Fail(id string) {
	dcaller.col.updEmittedTracked(-1)
	dcaller.dis.Fail(id)
}

func (dcaller *DispPatcherCaller) TimedOut(id string) {
	dcaller.col.updEmittedTracked(-1)
	dcaller.dis.TimedOut(id)
}

func (dcaller *DispPatcherCaller) Ack(id string) {
	dcaller.col.updEmittedTracked(-1)
	dcaller.dis.Ack(id)
}
