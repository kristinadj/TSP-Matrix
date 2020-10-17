package main

import (
	"container/heap"
	"math"
)

const (
	Infinity	= math.MaxFloat32
	Undefined	= -1
)

func (graph Graph) Dijkstra(sourceNode int) (cost map[int]float32, previous map[int]int) {
	cost = make(map[int]float32)
	previous = make(map[int]int)
	cost[sourceNode] = 0

	queue := &Queue {
		items: []int {},
		index: 	make(map[int]int),
		priority: make(map[int]float32),
	}

	for _, v := range graph.nodes {
		if v != sourceNode {
			cost[v] = Infinity
		}
		previous[v] =  Undefined
		queue.Add(v, cost[v])
	}

	for len(queue.items) != 0 {
		u := heap.Pop(queue).(int)
		for _, v := range graph.Neighbours(u) {
			alt := cost[u] + graph.Weight(u, v)
			if alt < cost[v] {
				cost[v] = alt
				previous[v] = u
				queue.Update(v, alt)
			}
		}
	}

	return cost, previous
}
