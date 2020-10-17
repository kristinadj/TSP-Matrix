package main

import (
	"fmt"
)

// TODO: If path does note exist...

type Graph struct {
	nodes 	[]int
	edges 	map[int]map[int]float32
}

func CreateGraph(url, weight string, polygons []PolygonDTO) (graph Graph) {
	graph = Graph {
		nodes: []int{},
		edges: make(map[int]map[int]float32),
	}

	var crossLocationsLinksNeighbourPolygons = getCrossLocationsBetweenNeighbourPolygons(fmt.Sprintf(
		"%s/matrix/crossLocationLinks/neighbourPolygons", url))

	for _, link := range crossLocationsLinksNeighbourPolygons {
		if weight == "distance" {
			graph.addEdge(link.FromLocationID, link.ToLocationID, link.Distance)
		} else {
			graph.addEdge(link.FromLocationID, link.ToLocationID, link.Duration)
		}
	}

	for _, polygon := range polygons {
		var locationsLinks = getLocationLinks(fmt.Sprintf(
			"%s/matrix/locationLinks/%d", url, polygon.ID), polygon.ID)
		for _, link := range locationsLinks.LocationLinks {
			if weight == "distance" {
				graph.addEdge(link.FromLocationID, link.ToLocationID, link.Distance)
			} else {
				graph.addEdge(link.FromLocationID, link.ToLocationID, link.Duration)
			}
		}
	}

	return graph
}


func (graph Graph) addEdge(u, v int, cost float32) {
	// TODO: Add nodes
	if _, ok := graph.edges[u]; !ok {
		// if edge does not exist, create it
		graph.edges[u] = make(map[int]float32)
	}
	// set cost for edge from u to v
	graph.edges[u][v] = cost
}

func (graph Graph) Neighbours(u int) (nodes []int){
	for v := range graph.edges[u] {
		nodes = append(nodes, v)
	}
	return nodes
}

func (graph Graph) Weight(u int, v int) float32 {
	return graph.edges[u][v]
}