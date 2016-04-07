package gopipe

import (
	"sync"
)

type Collector interface {
	Emit(map[string]interface{})
	AddOutput(chan map[string]interface{})
}

type TupleCollector struct {
	lock      *sync.Mutex
	stage     string
	out_chans []chan map[string]interface{}
}

func NewTupleCollector(stage string) *TupleCollector {
	tc := new(TupleCollector)
	tc.stage = stage
	tc.lock = new(sync.Mutex)
	return tc
}

func (tc *TupleCollector) Emit(tuple map[string]interface{}) {
	for _, chn := range tc.out_chans {
		chn <- tuple
	}
}

func (tc *TupleCollector) AddOutput(chn chan map[string]interface{}) {
	tc.lock.Lock()
	defer tc.lock.Unlock()
	for _, ch := range tc.out_chans {
		if ch == chn {
			return
		}
	}
	tc.out_chans = append(tc.out_chans, chn)
}
