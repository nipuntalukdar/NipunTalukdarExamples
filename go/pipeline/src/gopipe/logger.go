package gopipe

import (
	"bytes"
	"fmt"
	"github.com/Sirupsen/logrus"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"syscall"
	"time"
)

const (
	MAX_LOG_BUFFER    = 100 * 1024
	WRITE_SIZE        = 8000
	MAX_LOG_INTERVAL  = 2 * time.Second
	MAX_ROLLOVER_SIZE = 2 * 1024 * 1024 * 1024
)

type LogWriter struct {
	logs chan []byte
}

func NewLogWriter(inp chan []byte) *LogWriter {
	return &LogWriter{inp}
}

func (mywriter *LogWriter) Write(p []byte) (n int, err error) {
	mywriter.logs <- p
	return len(p), nil
}

type Logger struct {
	events  chan []byte
	outfile string
	file    *os.File
	buffer  *bytes.Buffer
	backups int
	outdir  string
	regxp   string
	writer  *LogWriter
	log     *logrus.Logger
	rolsize int
	fsize   int
}

func (logger *Logger) RollOver() {
	files, err := filepath.Glob(logger.regxp)
	if err != nil {
		fmt.Printf("Some error during rollover %v\n", err)
		os.Exit(1)
		return
	}
	fmt.Printf("Files  %v\n", files)

	var index_nums []int
	num_name := make(map[int]string)
	for _, file := range files {
		index_name := file[len(logger.outfile)+1:]
		if index_num, err := strconv.Atoi(index_name); err == nil {
			index_nums = append(index_nums, index_num)
			num_name[index_num] = file
		}
	}
	sort.Ints(index_nums)
	to_be_deleted := len(index_nums) - logger.backups + 1
	i := to_be_deleted
	if to_be_deleted > 0 {
		for ; to_be_deleted > 0; to_be_deleted-- {
			err = os.Remove(num_name[index_nums[len(index_nums)-to_be_deleted]])
			if err != nil && !os.IsNotExist(err) {
				fmt.Printf("Some error in removing file\n")
				os.Exit(1)
			}
		}
		index_nums = index_nums[:len(index_nums)-i]
	}
	i = len(index_nums)
	fmt.Printf(".... %v %v\n", index_nums, num_name)
	for i > 0 {
		err = os.Rename(num_name[index_nums[i-1]], fmt.Sprintf("%s.%d", logger.outfile, i+1))
		if err != nil {
			fmt.Printf("xxxError in renaming file %v\n", err)
		}
		i--
	}
	logger.file.Close()
	err = os.Rename(logger.outfile, fmt.Sprintf("%s.%d", logger.outfile, 1))
	if err != nil {
		fmt.Printf("Error in renaming file %v\n", err)
	}
	file := openAndLockFile(logger.outfile)
	fsize := GetFileSize(logger.outfile)
	if fsize < 0 {
		fmt.Printf("Unable to get file size\n")
		os.Exit(1)
	}
	logger.fsize = int(fsize)
	logger.file = file
}

func openAndLockFile(outfile string) *os.File {
	file, err := os.OpenFile(outfile, os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0644)
	if err != nil {
		fmt.Printf("Failed to open file:%s, err:%v\n", file, err)
		os.Exit(1)
	}
	fd := file.Fd()
	if syscall.Flock(int(fd), syscall.LOCK_EX|syscall.LOCK_NB) != nil {
		file.Close()
		fmt.Printf("Unable to lock log file\n")
		os.Exit(1)
	}

	return file
}

var LOG *logrus.Logger

func NewLogger() *Logger {
	outfile := "a.log"
	max_back_up := 10
	max_log_size := 256
	events := make(chan []byte, 40960)
	outdir := filepath.Dir(outfile)
	buf := make([]byte, MAX_LOG_BUFFER)
	buffer := bytes.NewBuffer(buf)
	buffer.Reset()
	file := openAndLockFile(outfile)
	fsize := GetFileSize(outfile)
	if fsize < 0 {
		fmt.Printf("Unable to get file size\n")
		os.Exit(1)
	}
	regexp := outfile + ".*"
	writer := NewLogWriter(events)
	logrloger := logrus.New()
	logrloger.Level = logrus.DebugLevel
	logrloger.Out = writer
	logrloger.Formatter = &logrus.TextFormatter{DisableColors: true,
		TimestampFormat: "2006-01-02T15:04:05"}
	LOG = logrloger
	return &Logger{events, outfile, file, buffer, max_back_up,
		outdir, regexp, writer, logrloger, max_log_size, int(fsize)}
}

var num int

func (logger *Logger) addMsg(msg []byte) {
	logger.buffer.Write(msg)
	if logger.buffer.Len() >= WRITE_SIZE {
		n, err := logger.file.Write(msg)
		if err != nil {
			fmt.Printf("Logging error\n")
			os.Exit(1)
		}
		logger.fsize += logger.buffer.Len()
		logger.buffer.Reset()
		logger.fsize += n
		if logger.fsize > logger.rolsize {
			fmt.Printf("Added %d %d %d\n", num, logger.fsize, logger.rolsize)
			num++
			logger.RollOver()
		}
	}
}

func logSyncer(logger *Logger) {
	for {
		msg := <-logger.events
		logger.addMsg(msg)
	}
}

func init() {
	num = 0
	logger := NewLogger()
	go logSyncer(logger)
}
