package gopipe

import (
	"fmt"
	"testing"
)

func TestConfig(t *testing.T) {
	config := GetConfig("a.yaml")
	val, ok := config.GetStrVal("pqr")
	if !ok {
		fmt.Printf("Failed to get config value")
	} else {
		fmt.Println(val)
	}
	ival, ok := config.GetIntVal("abc")
	if !ok {
		fmt.Printf("Failed to get config value")
	} else {
		fmt.Println(ival)
	}
}
