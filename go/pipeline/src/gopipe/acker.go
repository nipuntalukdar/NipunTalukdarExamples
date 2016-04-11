package gopipe

import (
	"math"
	"sync"
	"sync/atomic"
)

const max_parallel uint = 128

type Tracker interface {
	Fail(id string)
	Ack(id string)
}

type ackvalue struct {
	id  uint64
	val uint64
}

type Acker interface {
	AddAck(id uint64, val uint64)
	AddTracking(ids string)
}

type LocalAcker struct {
	currentTracks     []map[uint64]uint64
	currentTrackIds   []map[uint64]string
	numParallelTracks uint
	locks             []*sync.Mutex
	and_with          uint
	next_id           *uint64
	tracker           Tracker
	input_chan        chan *ackvalue
}

func NewAckValue(id uint64, value uint64) *ackvalue {
	val := new(ackvalue)
	val.id = id
	val.val = value
	return val
}

func NewLocalAcker(parallel uint, tracker Tracker) *LocalAcker {
	if parallel == 0 || parallel > max_parallel {
		parallel = max_parallel
	}

	lc := new(LocalAcker)
	var i uint = 0
	for ; i < parallel; i++ {
		lc.currentTracks = append(lc.currentTracks, make(map[uint64]uint64))
		lc.locks = append(lc.locks, new(sync.Mutex))
		lc.currentTrackIds = append(lc.currentTrackIds, make(map[uint64]string))
		lc.next_id = new(uint64)
	}
	lc.numParallelTracks = parallel
	i = parallel
	parallel = 0
	for {
		if i == 0 {
			break
		}
		i >>= 1
		parallel++
	}
	lc.and_with = uint(math.Pow(2, float64(parallel))) - 1
	lc.tracker = tracker
	lc.input_chan = make(chan *ackvalue, 102400)
	return lc
}

func (acker *LocalAcker) AddTracking(ids string) uint64 {
	id := atomic.AddUint64(acker.next_id, 1)
	index := (acker.and_with & uint(id)) % acker.numParallelTracks
	acker.locks[index].Lock()
	defer acker.locks[index].Unlock()
	acker.currentTracks[index][id] = 0
	acker.currentTrackIds[index][id] = ids
	return id
}

func (acker *LocalAcker) AddAck(id uint64, val uint64) {
	aval := NewAckValue(id, val)
	acker.input_chan <- aval
}

func (acker *LocalAcker) updateAck(id uint64, val uint64) {
	index := (acker.and_with & uint(id)) % acker.numParallelTracks
	acker.locks[index].Lock()
	defer acker.locks[index].Unlock()

	cval, ok := acker.currentTracks[index][id]
	if !ok {
		return
	}

	cval ^= val
	if cval != 0 {
		acker.currentTracks[index][id] = cval
	} else {
		delete(acker.currentTracks[index], id)
		ids := acker.currentTrackIds[index][id]
		delete(acker.currentTrackIds[index], id)
		acker.tracker.Ack(ids)
	}
}

func (acker *LocalAcker) Start() {
	num := acker.numParallelTracks
	for ; num > 0; num-- {
		go runAcker(acker)
	}
}

func runAcker(acker *LocalAcker) {
	for {
		aval := <-acker.input_chan
		acker.updateAck(aval.id, aval.val)
	}
}
