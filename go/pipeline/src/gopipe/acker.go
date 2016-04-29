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

type AckValue struct {
	id  uint64
	val uint64
}

type Acker interface {
	AddAck(id uint64, val uint64)
	AddTracking(ids string, trackerId uint) uint64
	AddTracker(id uint, tracker Tracker)
	SignalFail(id uint64)
	Start()
}

var ackerinst Acker

type trackIDs struct {
	trackerId uint
	ids       string
}

type LocalAcker struct {
	currentTracks     []map[uint64]uint64
	currentTrackIds   []map[uint64]*trackIDs
	numParallelTracks uint
	locks             []*sync.Mutex
	and_with          uint
	next_id           *uint64
	trackers          map[uint]Tracker
	input_chan        chan *AckValue
	timeout           int64
	exheap            *expiryHeap
}

func NewAckValue(id uint64, value uint64) *AckValue {
	return &AckValue{id, value}
}

func NewLocalAcker(parallel uint, timeout int64) *LocalAcker {
	if parallel == 0 || parallel > max_parallel {
		parallel = max_parallel
	}

	lc := new(LocalAcker)
	var i uint = 0
	for ; i < parallel; i++ {
		lc.currentTracks = append(lc.currentTracks, make(map[uint64]uint64))
		lc.locks = append(lc.locks, new(sync.Mutex))
		lc.currentTrackIds = append(lc.currentTrackIds, make(map[uint64]*trackIDs))
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
	lc.trackers = make(map[uint]Tracker)
	lc.input_chan = make(chan *AckValue, 102400)
	lc.timeout = timeout
	lc.exheap = NewExpiryHeap()
	return lc
}

func (acker *LocalAcker) AddTracking(ids string, tracker_id uint) uint64 {
	id := atomic.AddUint64(acker.next_id, 1)
	index := (acker.and_with & uint(id)) % acker.numParallelTracks
	acker.locks[index].Lock()
	defer acker.locks[index].Unlock()
	acker.currentTracks[index][id] = 0
	acker.currentTrackIds[index][id] = &trackIDs{tracker_id, ids}
	expval := &expiryValue{time.Now().Unix() + acker.timeout, id}
	acker.exheap.lock.Lock()
	heap.Push(acker.exheap, expval)
	acker.exheap.lock.Unlock()
	return id
}

func (acker *LocalAcker) SignalFail(id uint64) {
	acker.AddAck(id, fail_indicator)
}

func (acker *LocalAcker) AddAck(id uint64, val uint64) {
	LOG.Debugf("Added ack %d %d", id, val)
	aval := NewAckValue(id, val)
	acker.input_chan <- aval
}

func (acker *LocalAcker) AddTracker(id uint, tracker Tracker) {
	acker.trackers[id] = tracker
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
		trids := acker.currentTrackIds[index][id]
		delete(acker.currentTrackIds[index], id)
		acker.locks[index].Unlock()
		acker.trackers[trids.trackerId].Fail(trids.ids)
	} else {
		cval ^= val
		if cval != 0 {
			acker.currentTracks[index][id] = cval
			acker.locks[index].Unlock()
		} else {
			delete(acker.currentTracks[index], id)
			trids := acker.currentTrackIds[index][id]
			delete(acker.currentTrackIds[index], id)
			acker.locks[index].Unlock()
			acker.trackers[trids.trackerId].Ack(trids.ids)
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
	trids := acker.currentTrackIds[index][id]
	delete(acker.currentTrackIds[index], id)
	acker.locks[index].Unlock()
	LOG.Debugf("Timing out... %s", trids.ids)
	acker.trackers[trids.trackerId].TimedOut(trids.ids)
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
		acker.exheap.lock.Lock()
		expval, ret := acker.exheap.popIfLess(time.Now().Unix())
		acker.exheap.lock.Unlock()
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
	return &expiryHeap{[]*expiryValue{}, &sync.Mutex{}}
}

func (exh *expiryHeap) Len() int {
	return len(exh.expvals)
}

func (exh *expiryHeap) Less(i, j int) bool {
	return exh.expvals[i].timestamp < exh.expvals[j].timestamp
}

func (exh *expiryHeap) Swap(i, j int) {
	exh.expvals[i], exh.expvals[j] = exh.expvals[j], exh.expvals[i]
}

func (exh *expiryHeap) Push(x interface{}) {
	exh.expvals = append(exh.expvals, x.(*expiryValue))
}

func (exh *expiryHeap) Pop() interface{} {
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
	x := exh.expvals[0]
	if x.timestamp <= t {
		return heap.Pop(exh).(*expiryValue), true
	}
	return nil, false
}

func init() {
	ac := NewLocalAcker(8, 10)
	ackerinst = ac
	ackerinst.Start()
}

func GetAcker() Acker {
	return ackerinst
}
