package main

import (
	"encoding/csv"
	"fmt"
	"math"
	"os"
	"strconv"
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
		matrix := sequentialDijkstra(config, graph, polygons)
		exportMatrix(matrix, config.Weight)
	}
}

func exportMatrix(matrix map[int]map[int]float64, cost string) {
	file, _ := os.Create("output.csv")
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// define and write column headers
	headers := []string{
		"from",
		"to",
		cost,
	}
	writer.Write(headers)

	var l1Str string
	var l2Str string
	var costStr string

	for l1 := range matrix {
		for l2 := range matrix[l1] {
			r := make([]string, 0, 1+len(headers))
			l1Str = strconv.Itoa(l1)
			l2Str = strconv.Itoa(l2)
			costStr = strconv.Itoa(int(math.Round(matrix[l1][l2])))

			r = append(
				r,
				l1Str,
				l2Str,
				costStr,
			)

			writer.Write(r)
		}
	}
}

func sequentialDijkstra(config Configuration, graph Graph, polygons []PolygonDTO) (matrix map[int]map[int]float64) {
	matrix = make(map[int]map[int]float64)
	var polygonLocations = make(map[int][]int)

	// diagonal of matrix (POi links in same polygon)
	for _, polygon := range polygons {
		var pois = getPoiLinks(fmt.Sprintf(
			"%s/matrix/poiLinks/%d", config.Url, polygon.ID), polygon.ID)

		polygonLocations[polygon.ID] = pois.PoiIDS

		for _, link := range pois.LocationLinks {
			if matrix[link.FromLocationID] == nil {
				matrix[link.FromLocationID] = make(map[int]float64)
				matrix[link.FromLocationID][link.FromLocationID] = 0
			}
			if config.Weight == "distance" {
				matrix[link.FromLocationID][link.ToLocationID] = link.Distance

			} else {
				matrix[link.FromLocationID][link.ToLocationID] = link.Duration
			}
		}
	}

	// populating matrix - from location in one polygon to locations in other polygons
	for _, polygon1 := range polygons {
		// from location
		for _, from := range polygonLocations[polygon1.ID] {
			costs, _ := graph.Dijkstra(from)

			// to locations
			for _, polygon2 := range polygons {
				if polygon1.ID != polygon2.ID {
					for _, to := range polygonLocations[polygon2.ID] {
						if matrix[from] == nil {
							matrix[from] = make(map[int]float64)
						}
						matrix[from][to] = costs[to]
					}
				}
			}
		}
	}

	return matrix
}
