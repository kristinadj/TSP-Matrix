package main

type PolygonDTO struct {
	ID 			  		int `json:"id"`
	NeighboursIds 		[]int `json:"neighbours_ids"`
}

type CrossLocationLinksNeighbourPolygonsDTO struct {
	FromPolygonID 		int `json:"fromPolygon""`
	ToPolygonID 		int `json:"toPolygon""`
	FromLocationID 		int `json:"fromLocation""`
	ToLocationID 		int `json:"toLocation""`
	Distance			float32 `json:"distance""`
	Duration			float32 `json:"duration""`
}

type LocationLinksDTO struct {
	PolygonID 			int `json:"polygonId"`
	LocationLinks 		[]LinkDTO `json:"location_links"`
}

type PoiLinksDTO struct {
	PolygonID 			int `json:"polygonId"`
	PoiIDS		 		[]int `json:"poi_ids"`
	LocationLinks 		[]LinkDTO `json:"poi_links"`
}

type LinkDTO struct {
	FromLocationID 		int `json:"fromLocation"`
	ToLocationID 		int `json:"toLocation"`
	Distance			float32 `json:"distance"`
	Duration			float32 `json:"duration"`
}


