package gopipe

import (
	"fmt"
	"reflect"
)

var exreg *ExecutorRegistry

type ExecutorRegistry struct {
	registry map[string]Executor
}

func (reg *ExecutorRegistry) AddType(name string, executor Executor) {
	reg.registry[name] = executor
}

func GetRegistry() *ExecutorRegistry {
	return exreg
}

func (reg *ExecutorRegistry) GetInstance(name string) *Executor {
	class, found := reg.registry[name]
	if !found {
		return nil
	}

	class_type := reflect.TypeOf(class)
	fmt.Printf("%v\n", class_type)
	instance := reflect.New(class_type)
	fmt.Printf("%v\n", instance)
	instance2 := instance.Elem()
	executor_instance := instance2.Interface().(Executor)

	return &executor_instance
}

func init() {
	fmt.Println("Initializing executor registry")
	exreg = new(ExecutorRegistry)
	exreg.registry = make(map[string]Executor)
}
