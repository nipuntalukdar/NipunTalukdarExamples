package main

import (
	"fmt"

	hclog "github.com/hashicorp/go-hclog"
	"github.com/nipuntalukdar/rollingwriter"
)

func main() {
	config := rollingwriter.NewDefaultConfig()
	writer, err := rollingwriter.NewWriterFromConfig(&config)
	if err != nil {
		panic(err)
	}
	logger := hclog.New(&hclog.LoggerOptions{Name: "RollingHCLog", Output: writer,
	Level: hclog.Debug,})
	for i := 0; i < 10; i++ {
		fmt.Println(i)
		logger.Debug("Hello", "a", "message for a")
		logger.Info("Hello", "b", "message for b")
	}
	writer.Close()
}
