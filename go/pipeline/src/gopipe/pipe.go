package gopipe

import (
	"fmt"
	"hash/crc32"
	"sync"
)

type Collector interface {
	Emit(tuple map[string]interface{}, context interface{})
	Ack(context interface{})
	Fail(context interface{})
	AddOutput(outchan chan *OutPut)
	IsForDispatcher() bool
}

type groupedChans struct {
	out_stg_name string
	groupKeys    []string
	chan_count   uint32
	chans        []chan *OutPut
}

type TupleCollector struct {
	lock           *sync.Mutex
	stage          string
	id             uint64
	out_chans      []chan *OutPut
	isdisp         uint
	groupd_chans   []*groupedChans
	all_group_keys []string
	num_grouped    int
}

func getKeyHash(key string) uint32 {
	return crc32.ChecksumIEEE([]byte(key))
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
	ret.groupd_chans = tc.groupd_chans
	ret.all_group_keys = tc.all_group_keys
	ret.num_grouped = tc.num_grouped
	return ret
}

func (tc *TupleCollector) emitTrack(tuple map[string]interface{}, context *AckValue) {
	emittedVal := tc.id
	outval := uint64(0)
	var out *OutPut = nil
	if context == nil {
		out = &OutPut{tuple, nil}
	}
	for _, chn := range tc.out_chans {
		if out == nil {
			emittedVal++
			outval ^= emittedVal
			chn <- &OutPut{tuple, &AckValue{context.id, emittedVal}}
		} else {
			chn <- out
		}
	}
	if tc.num_grouped > 0 {
		var hashCode uint32 = 0
		// first check if all the group keys are there
		for _, k := range tc.all_group_keys {
			_, ok := tuple[k]
			if !ok {
				panic(fmt.Sprintf("Grouping key %s is missing", k))
				return
			}
		}
		for _, groupd_chan := range tc.groupd_chans {
			hashCode = 0
			for _, grKey := range groupd_chan.groupKeys {
				hashCode ^= getKeyHash(tuple[grKey].(string))
			}
			if out != nil {
				groupd_chan.chans[hashCode%groupd_chan.chan_count] <- out
			} else {
				emittedVal++
				outval ^= emittedVal
				groupd_chan.chans[hashCode%groupd_chan.chan_count] <- &OutPut{tuple,
					&AckValue{context.id, emittedVal}}
			}
		}
	}
	if context != nil {
		GetAcker().AddAck(context.id, outval)
	}
}

func (tc *TupleCollector) Emit(tuple map[string]interface{}, context interface{}) {
	if len(tc.out_chans) == 0 && tc.num_grouped == 0 {
		return
	}
	if context != nil {
		if tc.IsForDispatcher() {
			tuple_uuid := context.(string)
			id := GetAcker().AddTracking(tuple_uuid, tc.isdisp)
			LOG.Debugf("Added tracking %s %d", tuple_uuid, id)
			tc.emitTrack(tuple, &AckValue{id, 0})
		} else {
			tc.emitTrack(tuple, context.(*AckValue))
		}
	} else {
		tc.emitTrack(tuple, nil)
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
