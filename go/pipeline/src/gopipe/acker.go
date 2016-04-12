package gopipe

import (
	"container/heap"
	"math"
	"sync"
	"sync/atomic"
	"time"
)

const max_parallel uint = 128
const fail_indicator uint64 = math.MaxUint64

type Tracker interface {
	Fail(id string)
	Ack(id string)
	TimedOut(id string)
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
	timeout           int64
	exheap            *expiryHeap
}

func NewAckValue(id uint64, value uint64) *ackvalue {
	val := new(ackvalue)
	val.id = id
	val.val = value
	return val
}

func NewLocalAcker(parallel uint, tracker Tracker, timeout int64) *LocalAcker {
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
	lc.timeout = timeout
	lc.exheap = NewExpiryHeap()
	return lc
}

func (acker *LocalAcker) AddTracking(ids string) uint64 {
	id := atomic.AddUint64(acker.next_id, 1)
	index := (acker.and_with & uint(id)) % acker.numParallelTracks
	acker.locks[index].Lock()
	defer acker.locks[index].Unlock()
	acker.currentTracks[index][id] = 0
	acker.currentTrackIds[index][id] = ids
	expval := new(expiryValue)
	expval.id = id
	expval.timestamp = time.Now().Unix() + acker.timeout
	heap.Push(acker.exheap, expval)
	return id
}

func (acker *LocalAcker) SignalFail(id uint64) {
	acker.AddAck(id, fail_indicator)
}

func (acker *LocalAcker) AddAck(id uint64, val uint64) {
	aval := NewAckValue(id, val)
	acker.input_chan <- aval
}

func (acker *LocalAcker) updateAck(id uint64, val uint64) {
	index := (acker.and_with & uint(id)) % acker.numParallelTracks
	acker.locks[index].Lock()

	cval, ok := acker.currentTracks[index][id]
	if !ok {
		acker.locks[index].Unlock()
		return
	}

	if val == fail_indicator {
		delete(acker.currentTracks[index], id)
		ids := acker.currentTrackIds[index][id]
		delete(acker.currentTrackIds[index], id)
		acker.locks[index].Unlock()
		acker.tracker.Fail(ids)
	} else {
		cval ^= val
		if cval != 0 {
			acker.currentTracks[index][id] = cval
			acker.locks[index].Unlock()
		} else {
			delete(acker.currentTracks[index], id)
			ids := acker.currentTrackIds[index][id]
			delete(acker.currentTrackIds[index], id)
			acker.locks[index].Unlock()
			acker.tracker.Ack(ids)
		}
	}
}

func (acker *LocalAcker) handleTimeOut(id uint64) {
	index := (acker.and_with & uint(id)) % acker.numParallelTracks
	acker.locks[index].Lock()

	_, ok := acker.currentTracks[index][id]
	if !ok {
		acker.locks[index].Unlock()
		return
	}
	delete(acker.currentTracks[index], id)
	ids := acker.currentTrackIds[index][id]
	delete(acker.currentTrackIds[index], id)
	acker.locks[index].Unlock()
	acker.tracker.TimedOut(ids)
}

func (acker *LocalAcker) Start() {
	num := acker.numParallelTracks
	for ; num > 0; num-- {
		go runAcker(acker)
	}
	go expiryChecker(acker)
}

func runAcker(acker *LocalAcker) {
	for {
		aval := <-acker.input_chan
		acker.updateAck(aval.id, aval.val)
	}
}

func expiryChecker(acker *LocalAcker) {
	time.Sleep(1 * time.Second)
	for {
		expval, ret := acker.exheap.popIfLess(time.Now().Unix())
		if !ret {
			time.Sleep(1 * time.Second)
			continue
		}
		acker.handleTimeOut(expval.id)
	}
}

type expiryValue struct {
	timestamp int64
	id        uint64
}

type expiryHeap struct {
	expvals []*expiryValue
	lock    *sync.Mutex
}

func NewExpiryHeap() *expiryHeap {
	exh := new(expiryHeap)
	exh.lock = new(sync.Mutex)
	return exh
}

func (exh *expiryHeap) Len() int {
	exh.lock.Lock()
	defer exh.lock.Unlock()
	return len(exh.expvals)
}

func (exh *expiryHeap) Less(i, j int) bool {
	exh.lock.Lock()
	defer exh.lock.Unlock()
	return exh.expvals[i].timestamp < exh.expvals[j].timestamp
}

func (exh *expiryHeap) Swap(i, j int) {
	exh.lock.Lock()
	defer exh.lock.Unlock()
	exh.expvals[i], exh.expvals[j] = exh.expvals[j], exh.expvals[i]
}

func (exh *expiryHeap) Push(x interface{}) {
	exh.lock.Lock()
	defer exh.lock.Unlock()
	exh.expvals = append(exh.expvals, x.(*expiryValue))
}

func (exh *expiryHeap) Pop() interface{} {
	exh.lock.Lock()
	defer exh.lock.Unlock()
	vals := exh.expvals
	n := len(vals)
	if n == 0 {
		return nil
	}
	x := exh.expvals[n-1]
	exh.expvals = exh.expvals[0 : n-1]
	return x
}

func (exh *expiryHeap) popIfLess(t int64) (*expiryValue, bool) {
	if exh.Len() == 0 {
		return nil, false
	}
	exh.lock.Lock()
	l := len(exh.expvals)
	x := exh.expvals[l-1]
	exh.lock.Unlock()
	if x.timestamp <= t {
		return heap.Pop(exh).(*expiryValue), true
	}
	return nil, false
}
