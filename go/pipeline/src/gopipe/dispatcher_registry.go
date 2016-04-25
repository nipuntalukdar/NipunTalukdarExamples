package gopipe

import (
	"fmt"
	"reflect"
)

var dispreg *DispatcherRegistry

type DispatcherRegistry struct {
	registry map[string]Dispatcher
}

func (reg *DispatcherRegistry) AddType(name string, disp Dispatcher) {
	type_disp := reflect.TypeOf(disp).Elem()
	reg.registry[name] = reflect.New(type_disp.(reflect.Type)).Interface().(Dispatcher)
}

func GetDispRegistry() *DispatcherRegistry {
	return dispreg
}

func (reg *DispatcherRegistry) GetInstance(name string) Dispatcher {
	class, found := reg.registry[name]
	if !found {
		return nil
	}
	x := reflect.TypeOf(class).Elem()
	y := reflect.New(x.(reflect.Type))
	z := y.Interface().(Dispatcher)
	return z
}

func init() {
	fmt.Println("Initializing Dispatcher registry")
	dispreg = new(DispatcherRegistry)
	dispreg.registry = make(map[string]Dispatcher)
}
