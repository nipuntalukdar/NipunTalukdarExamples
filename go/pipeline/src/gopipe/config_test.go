package gopipe

import (
	"fmt"
	"testing"
)

func TestConfig(t *testing.T) {
	config := GetConfig()
	val, ok := config.GetStrVal("log_path")
	if !ok {
		fmt.Printf("Failed to get config value")
	} else {
		fmt.Println(val)
	}
	ival, ok := config.GetIntVal("max_unacked")
	if !ok {
		fmt.Printf("Failed to get config value")
	} else {
		fmt.Println(ival)
	}
}
