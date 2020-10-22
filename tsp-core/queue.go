package main

import "container/heap"

type Queue struct {
	items 			[]int
	index 			map[int]int
	priority		map[int]float64
}

func (queue *Queue) Len() int {
	return len(queue.items)
}

func (queue *Queue) Less(i, j int) bool {
	return  queue.priority[queue.items[i]] < queue.priority[queue.items[j]]
}

func (queue *Queue) Swap(i, j int) {
	queue.items[i], queue.items[j] = queue.items[j], queue.items[i]
	queue.index[queue.items[i]] = i
	queue.index[queue.items[j]] = j
}

func (queue *Queue) Push(x interface{}) {
	n := len(queue.items)
	item := x.(int)
	queue.index[item] = n
	queue.items = append(queue.items, item)
}

func (queue *Queue) Pop() interface{} {
	oldItems := queue.items
	n := len(oldItems)
	item := oldItems[n-1]
	queue.index[item] = -1
	queue.items = oldItems[0 : n-1]
	return item
}

func (queue *Queue) Add(item int, priority float64) {
	heap.Push(queue, item)
	queue.Update(item, priority)
}

func (queue *Queue) Update(item int, priority float64) {
	queue.priority[item] = priority
	heap.Fix(queue, queue.index[item])
}




