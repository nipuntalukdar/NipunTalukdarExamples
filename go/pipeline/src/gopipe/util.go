package gopipe

import (
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
