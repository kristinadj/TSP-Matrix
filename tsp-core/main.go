package main

import (
	"fmt"
)

type Configuration struct {
	Url    string `json:"geoApiUrl"`
	Weight string `json:"weight"`
	ParallelImplementation bool `json:"parallel_implementation"`
}

func main() {
	fmt.Println("Starting the application...")
	var config = ReadConfig()

	var polygons = getPolygons(fmt.Sprintf("%s/polygon", config.Url))
	graph := CreateGraph(config.Url, config.Weight, polygons)

	if !config.ParallelImplementation {
		sequentialDijkstra(config, graph, polygons)
	}
}

func sequentialDijkstra(config Configuration, graph Graph, polygons []PolygonDTO) (matrix map[int]map[int]float32) {
	matrix = make(map[int]map[int]float32)
	var locations []int

	for _, polygon := range polygons {
		var pois = getPoiLinks(fmt.Sprintf(
			"%s/matrix/poiLinks/%d", config.Url, polygon.ID), polygon.ID)
		locations = append(locations, pois.PoiIDS...)
		for _, link := range pois.LocationLinks {
			if config.Weight == "distance" {
				matrix[link.FromLocationID][link.ToLocationID] = link.Distance
			} else {
				matrix[link.FromLocationID][link.ToLocationID] = link.Duration
			}
		}
	}

	for _, l1 := range locations {
		costs, _ := graph.Dijkstra(l1)
		for _, l2 := range locations {
			if l1 != l2 && matrix[l1][l2] != 0 {
				matrix[l1][l2] = costs[l2]
			}
		}
	}

	return matrix
}
