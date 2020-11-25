package main

import (
	"encoding/csv"
	"fmt"
	"math"
	"os"
	"strconv"
	"sync"
)


func GetTSPMatrixSequential(config Configuration, graph Graph, polygons []PolygonDTO) (matrix map[int]map[int]float64) {
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

func GetTSPMatrixParallel(config Configuration, graph Graph, polygons []PolygonDTO) (matrix map[int]map[int]float64) {
	matrix = make(map[int]map[int]float64)
	var polygonLocations = make(map[int][]int)

	// diagonal of matrix (POi links in same polygon)
	var wg sync.WaitGroup
	poiLinksList := make([]*PoiLinksDTO, len(polygons))
	for i, polygon := range polygons {
		wg.Add(1)
		go func(i int, polygon PolygonDTO) {
			defer wg.Done()
			var poiLinks = getPoiLinks(fmt.Sprintf(
				"%s/matrix/poiLinks/%d", config.Url, polygon.ID), polygon.ID)
			poiLinksList[i] = &poiLinks
		}(i, polygon)
	}
	wg.Wait()

	for _, item := range poiLinksList {
		polygonLocations[item.PolygonID] = item.PoiIDS
		for _, link := range item.LocationLinks {
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

func ExportMatrix(matrix map[int]map[int]float64, cost string, isParallel bool) {
	var fileName string
	if isParallel {
		fileName = "output-parallel.csv"
	} else {
		fileName = "output-sequential.csv"
	}

	file, _ := os.Create(fileName)
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

