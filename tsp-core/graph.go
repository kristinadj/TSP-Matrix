package main

import (
	"fmt"
	"sync"
)

type Graph struct {
	nodes 		[]int
	_nodes		map[int]struct{}
	edges 		map[int]map[int]float64
}

func CreateGraphSequential(url, weight string, polygons []PolygonDTO) (graph Graph) {
	graph = Graph {
		nodes: []int{},
		_nodes: make(map[int]struct{}),
		edges: make(map[int]map[int]float64),
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

	graph.nodes = make([]int, 0, len(graph._nodes))
	for nodeId := range graph._nodes {
		graph.nodes = append(graph.nodes, nodeId)
	}

	return graph
}

func CreateGraphParallel(url, weight string, polygons []PolygonDTO) (graph Graph) {
	graph = Graph {
		nodes: []int{},
		_nodes: make(map[int]struct{}),
		edges: make(map[int]map[int]float64),
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

	var wg sync.WaitGroup
	locationsLinksList := make([]*LocationLinksDTO, len(polygons))
	for i, polygon := range polygons {
		wg.Add(1)
		go func(i int, polygon PolygonDTO) {
			defer wg.Done()
			var locationsLinks = getLocationLinks(fmt.Sprintf(
				"%s/matrix/locationLinks/%d", url, polygon.ID), polygon.ID)
			locationsLinksList[i] = &locationsLinks
		}(i, polygon)
	}
	wg.Wait()

	for _, item := range locationsLinksList {
		for _, link := range item.LocationLinks {
			if weight == "distance" {
				graph.addEdge(link.FromLocationID, link.ToLocationID, link.Distance)
			} else {
				graph.addEdge(link.FromLocationID, link.ToLocationID, link.Duration)
			}
		}
	}

	graph.nodes = make([]int, 0, len(graph._nodes))
	for nodeId := range graph._nodes {
		graph.nodes = append(graph.nodes, nodeId)
	}

	return graph
}

func (graph Graph) addEdge(u, v int, cost float64) {
	graph._nodes[u] = struct{}{}
	graph._nodes[v] = struct{}{}

	if _, ok := graph.edges[u]; !ok {
		// if edge does not exist, create it
		graph.edges[u] = make(map[int]float64)
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

func (graph Graph) Weight(u int, v int) float64 {
	return graph.edges[u][v]
}