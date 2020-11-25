package main

import (
	"fmt"
	"time"
)

type Configuration struct {
	Url    string `json:"geoApiUrl"`
	Weight string `json:"weight"`
	ParallelImplementation bool `json:"parallel_implementation"`
}

func main() {
	fmt.Println("Starting the application...")
	var config = ReadConfig()

	start := time.Now()

	var polygons = getPolygons(fmt.Sprintf("%s/polygon", config.Url))

	if !config.ParallelImplementation {
		graph := CreateGraphSequential(config.Url, config.Weight, polygons)
		matrix := GetTSPMatrixSequential(config, graph, polygons)
		ExportMatrix(matrix, config.Weight, config.ParallelImplementation)
	} else {
		graph := CreateGraphParallel(config.Url, config.Weight, polygons)
		matrix := GetTSPMatrixParallel(config, graph, polygons)
		ExportMatrix(matrix, config.Weight, config.ParallelImplementation)
	}

	duration := time.Since(start)
	fmt.Printf("Total time: %f seconds \n", duration.Seconds())
}


