package gopipe

import (
	"crypto/rand"
	"fmt"
	"os"
	"syscall"
)

func GetFileSize(path string) int64 {
	var st syscall.Stat_t
	err := syscall.Stat(path, &st)
	if err != nil {
		return -1
	}
	return st.Size
}

func GetFileSizeFile(file *os.File) int64 {
	filestat, err := file.Stat()
	if err != nil {
		return -1
	}
	return filestat.Size()
}

type UUID struct {
	lsb uint64
	msb uint64
}

func NewUUID(inp []byte) *UUID {
	if len(inp) != 16 {
		panic("Length of input array for UUID must be 16")
	}
	var msb uint64 = 0
	var lsb uint64 = 0
	i := 0
	for ; i < 8; i++ {
		msb = (msb << 8) | uint64(inp[i]&0xff)
	}
	for ; i < 16; i++ {
		lsb = (lsb << 8) | uint64(inp[i]&0xff)
	}

	return &UUID{lsb, msb}
}

func NewRandomUUID() *UUID {
	b := make([]byte, 16)
	_, err := rand.Read(b)
	if err != nil {
		return nil
	}
	return NewUUID(b)
}

func NewRandomUUIDStr() string {
	uuid := NewRandomUUID()
	return fmt.Sprintf("%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x",
		(uuid.msb>>56)&255,
		(uuid.msb>>48)&255,
		(uuid.msb>>40)&255,
		(uuid.msb>>32)&255,
		(uuid.msb>>24)&255,
		(uuid.msb>>16)&255,
		(uuid.msb>>8)&255,
		uuid.msb&255,
		(uuid.lsb>>56)&255,
		(uuid.lsb>>48)&255,
		(uuid.lsb>>40)&255,
		(uuid.lsb>>32)&255,
		(uuid.lsb>>24)&255,
		(uuid.lsb>>16)&255,
		(uuid.lsb>>8)&255,
		uuid.lsb&255)
}
