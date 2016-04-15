package gopipe

import (
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"sync"
)

const (
	INVALID_VAL_INT = -1
	INVALID_VAL_STR = ""
)

type Config struct {
	file   string
	params map[string]interface{}
}

var config *Config
var once sync.Once
var configFile string

func initConfig(file string) {
	b, err := ioutil.ReadFile(file)
	if err != nil {
		panic(err)
	}
	configFile = file
	var output map[string]interface{}
	LOG.Info(b)
	err = yaml.Unmarshal(b, &output)
	if err != nil {
		panic(err)
	}
	config = &Config{file, output}

}

func GetConfig(file string) *Config {
	once.Do(func() { initConfig(file) })
	return config
}

func (config *Config) GetIntVal(key string) (int, bool) {
	val, ok := config.params[key]
	if !ok {
		return INVALID_VAL_INT, false
	}
	return val.(int), true
}

func (config *Config) GetStrVal(key string) (string, bool) {
	val, ok := config.params[key]
	if !ok {
		return INVALID_VAL_STR, false
	}
	return val.(string), true
}
