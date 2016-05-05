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
	type_ex := reflect.TypeOf(executor).Elem()
	reg.registry[name] = reflect.New(type_ex.(reflect.Type)).Interface().(Executor)
}

func GetRegistry() *ExecutorRegistry {
	return exreg
}

func (reg *ExecutorRegistry) GetInstance(name string) Executor {
	class, found := reg.registry[name]
	if !found {
		return nil
	}
	x := reflect.TypeOf(class).Elem()
	y := reflect.New(x.(reflect.Type))
	z := y.Interface().(Executor)

	return z
}

func init_executor_reg() {
	fmt.Println("Initializing executor registry")
	exreg = new(ExecutorRegistry)
	exreg.registry = make(map[string]Executor)
}
