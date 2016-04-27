package gopipe

import "sync/atomic"

type NextIdGetter struct {
	next_id *uint32
}

func NewNextIdGettr(initial_value uint32) *NextIdGetter {
	x := new(uint32)
	*x = initial_value

	return &NextIdGetter{x}
}

func (next *NextIdGetter) NextId() uint {
	next_id := atomic.AddUint32(next.next_id, 1)
	return uint(next_id)
}
