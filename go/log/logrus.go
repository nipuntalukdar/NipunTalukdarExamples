package main

import (
	"bytes"
	"fmt"
	"github.com/Sirupsen/logrus"
	"io/ioutil"
	"os"
	"syscall"
	"time"
)

type MyIoWriter struct {
	outfile string
	file    *os.File
	buffer  *bytes.Buffer
}

func (myio *MyIoWriter) Write(p []byte) (n int, err error) {
	n, err = myio.buffer.Write(p)
	if err != nil || n != len(p) {
		panic("Write error")
	}
	n1 := myio.buffer.Len()
	if n1 > 1280 {
		n2, err := myio.file.Write(myio.buffer.Bytes())
		if err != nil || n1 != n2 {
			panic("Write error")
		}
		myio.buffer.Reset()
	}

	return n, err
}

func NewMyIoWriter(outfile string) *MyIoWriter {
	buf := make([]byte, 2560)
	buffer := bytes.NewBuffer(buf)
	buffer.Reset()
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

	files, err := ioutil.ReadDir("/home/geet/work/NipunTalukdarExamples/go")
	if err != nil {
		fmt.Printf("Unable to read the dir\n")
		os.Exit(1)
	}

	for _, fino := range files {
		fmt.Printf("File %s\n", fino.Name())
	}

	return &MyIoWriter{outfile, file, buffer}
}

func main() {
	log := logrus.New()
	log.Formatter = &logrus.TextFormatter{DisableColors: true,
		TimestampFormat: "2006-01-02T15:04:05"}
	log.Level = logrus.DebugLevel
	//mywriter := NewMyIoWriter("test.txt")
	mywriter := os.Stdout
	log.Out = mywriter
	for {
		log.Debugf("Hello world, you are so beautiful %s", "yes")
		time.Sleep(250 * time.Millisecond)
	}
}
