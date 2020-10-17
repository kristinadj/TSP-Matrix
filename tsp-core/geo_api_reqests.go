package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

func getPolygons(url string) []PolygonDTO {
	fmt.Println("Getting polygons")
	fmt.Printf("Calling %s\n", url)
	response, err := http.Get(url)
	if err != nil {
		fmt.Printf("The HTTP request failed with error %s\n", err)
		os.Exit(-1)
	} else {
		data, _ := ioutil.ReadAll(response.Body)
		var polygons []PolygonDTO
		json.Unmarshal(data, &polygons)
		fmt.Println("Finished getting polygons")
		return polygons
	}
	return []PolygonDTO{}
}

func getCrossLocationsBetweenNeighbourPolygons(url string) []CrossLocationLinksNeighbourPolygonsDTO {
	fmt.Println("Getting data on distance/duration between cross locations from neighbouring polygons")
	fmt.Printf("Calling %s\n", url)
	response, err := http.Get(url)
	if err != nil {
		fmt.Printf("The HTTP request failed with error %s\n", err)
		os.Exit(-1)
	} else {
		data, _ := ioutil.ReadAll(response.Body)
		var crossLocationsLinks []CrossLocationLinksNeighbourPolygonsDTO
		json.Unmarshal(data, &crossLocationsLinks)
		fmt.Println("Finished getting data on cross locations from neighbouring polygons")
		return crossLocationsLinks
	}
	return []CrossLocationLinksNeighbourPolygonsDTO{}
}

func getLocationLinks(url string, polygonId int) LocationLinksDTO {
	fmt.Printf("Getting data on distance/duration between cross locations, POI and cross locations and vice " +
		"versa within a polygon %d\n", polygonId)
	fmt.Printf("Calling %s\n", url)
	response, err := http.Get(url)
	if err != nil {
		fmt.Printf("The HTTP request failed with error %s\n", err)
		os.Exit(-1)
	} else {
		data, _ := ioutil.ReadAll(response.Body)
		var locationLinks LocationLinksDTO
		json.Unmarshal(data, &locationLinks)
		fmt.Printf("Finished getting data on locations within a polygon %d\n", polygonId)
		return locationLinks
	}
	return LocationLinksDTO{}
}

func getPoiLinks(url string, polygonId int) PoiLinksDTO {
	fmt.Printf("Getting data on distance/duration between POIs within a polygon %d\n", polygonId)
	fmt.Printf("Calling %s\n", url)
	response, err := http.Get(url)
	if err != nil {
		fmt.Printf("The HTTP request failed with error %s\n", err)
		os.Exit(-1)
	} else {
		data, _ := ioutil.ReadAll(response.Body)
		var poiLinks PoiLinksDTO
		json.Unmarshal(data, &poiLinks)
		fmt.Printf("Finished getting data on POIs within a polygon %d\n", polygonId)
		return poiLinks
	}
	return PoiLinksDTO{}
}
