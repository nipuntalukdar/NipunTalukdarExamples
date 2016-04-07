package gopipe

import (
	"fmt"
)

var eventstr chan string

type Logger struct {
	events chan string
}

func Log(log string) {
	LoggerInstance.events <- log
}

var LoggerInstance *Logger

func run(logger *Logger) {
	for {
		msg := <-logger.events
		fmt.Print(msg)
	}
}

func init() {
	LoggerInstance = new(Logger)
	LoggerInstance.events = make(chan string, 1024)
	go run(LoggerInstance)
}
