package gopipe

import (
	"sync"
)

type Collector interface {
	Emit(tuple map[string]interface{}, context interface{})
	Ack(context interface{})
	Fail(context interface{})
	AddOutput(outchan chan *OutPut)
	IsForDispatcher() bool
}

type TupleCollector struct {
	lock      *sync.Mutex
	stage     string
	id        uint64
	out_chans []chan *OutPut
	isdisp    uint
}

func NewTupleCollector(stage string, id uint, isdisp uint) *TupleCollector {
	tc := new(TupleCollector)
	tc.stage = stage
	tc.id = uint64(id) << 32
	tc.lock = &sync.Mutex{}
	tc.isdisp = isdisp
	return tc
}

func (tc *TupleCollector) Copy() *TupleCollector {
	ret := new(TupleCollector)
	ret.lock = &sync.Mutex{}
	ret.stage = tc.stage
	ret.id = tc.id
	ret.out_chans = tc.out_chans
	ret.isdisp = tc.isdisp
	return ret
}

func (tc *TupleCollector) emitTrack(tuple map[string]interface{}, context *AckValue) {
	id := context.id
	emittedVal := tc.id
	outval := uint64(0)
	for _, chn := range tc.out_chans {
		emittedVal++
		outval ^= emittedVal
		chn <- &OutPut{tuple, &AckValue{id, emittedVal}}
	}
	GetAcker().AddAck(id, outval)
}

func (tc *TupleCollector) Emit(tuple map[string]interface{}, context interface{}) {
	if len(tc.out_chans) == 0 {
		return
	}
	if context == nil {
		for _, chn := range tc.out_chans {
			chn <- &OutPut{tuple, nil}
		}
	} else {
		if tc.IsForDispatcher() {
			tuple_uuid := context.(string)
			id := GetAcker().AddTracking(tuple_uuid, tc.isdisp)
			LOG.Infof("Added tracking %s %d", tuple_uuid, id)
			tc.emitTrack(tuple, &AckValue{id, 0})
		} else {
			tc.emitTrack(tuple, context.(*AckValue))
		}
	}
}

func (tc *TupleCollector) Ack(context interface{}) {
	if context == nil {
		return
	}
	ackval := context.(*AckValue)
	GetAcker().AddAck(ackval.id, ackval.val)
}

func (tc *TupleCollector) Fail(context interface{}) {
	if context == nil {
		return
	}
	ackval := context.(*AckValue)
	GetAcker().SignalFail(ackval.id)
}

func (tc *TupleCollector) AddOutput(chn chan *OutPut) {
	tc.lock.Lock()
	defer tc.lock.Unlock()
	for _, ch := range tc.out_chans {
		if ch == chn {
			return
		}
	}
	tc.out_chans = append(tc.out_chans, chn)
}

func (tc *TupleCollector) IsForDispatcher() bool {
	return tc.isdisp > 0
}
