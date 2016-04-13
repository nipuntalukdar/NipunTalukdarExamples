package main

import (
	"bytes"
	"fmt"
	"github.com/Sirupsen/logrus"
	"time"
)

type MyIoWriter struct {
	buffer *bytes.Buffer
}

func (myio *MyIoWriter) Write(p []byte) (n int, err error) {
	n, err = myio.buffer.Write(p)
	if err != nil {
		panic("Write error")
	}
	if myio.buffer.Len() > 1280 {
		fmt.Printf("%s\n", myio.buffer.Bytes())
		myio.buffer.Reset()
	}

	return n, err
}

func NewMyIoWriter() *MyIoWriter {
	buf := make([]byte, 2560)
	buffer := bytes.NewBuffer(buf)
	buffer.Reset()
	return &MyIoWriter{buffer}
}

func main() {
	log := logrus.New()
	log.Formatter = &logrus.TextFormatter{DisableColors: true,
		TimestampFormat: "2006-01-02T15:04:05"}
	log.Level = logrus.DebugLevel
	mywriter := NewMyIoWriter()
	log.Out = mywriter
	for {
		log.Debug("Hello world, you are so beautiful")
		time.Sleep(1 * time.Second)
	}
}
