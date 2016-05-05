package gopipe

import (
	"fmt"
	"os"
)

var HOME string = "PIPELINE_HOME"
var CONFIG_DIR string = ""

func getConfigDir() string {
	return CONFIG_DIR
}

func init() {
	home := os.Getenv(HOME)
	if home == "" {
		home = "/tmp"
	}
	CONFIG_DIR = home + "/" + "configs"
	fileInfo, err := os.Stat(CONFIG_DIR)
	if err != nil {
		panic(err)
	}
	if !fileInfo.IsDir() {
		panic(fmt.Sprintf("%s is not directory or it doesn't exist"))
	}
	configFile := CONFIG_DIR + "/configs.yaml"
	initConfig(configFile)
	init_logger()
	init_acker()
	init_disp_reg()
	init_executor_reg()
	init_stages()
}
