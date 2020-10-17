package main

import (
	"encoding/json"
	"os"
)

func ReadConfig() Configuration {
	file, _ := os.Open("config.json")
	defer file.Close()
	decoder := json.NewDecoder(file)
	configuration := Configuration{}
	err := decoder.Decode(&configuration)
	if err != nil {
		panic("Invalid config file")
	}
	if configuration.Weight != "distance" && configuration.Weight != "duration" {
		panic("Invalid value for weight parameter")
	}
	return configuration
}
