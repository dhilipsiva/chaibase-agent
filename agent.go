package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/ds-forks/bugst-go-serial"
)

func writeHandler(w http.ResponseWriter, m map[string]string) {
	jsonString, err := json.Marshal(m)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(err.Error()))
	} else {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(jsonString))
	}
}

func handler(w http.ResponseWriter, r *http.Request) {
	m := make(map[string]string)
	m["ping"] = "pong"
	writeHandler(w, m)
	// fmt.Fprintf(w, "Hi there, I love %s!", r.URL.Path[1:])
}

func main() {
	//http.HandleFunc("/", handler)
	//http.ListenAndServe(":9876", nil)
	ports, err := serial.GetPortsList()
	if err != nil {
		log.Fatal(err)
	}
	if len(ports) == 0 {
		fmt.Println("No serial ports found!")
	} else {
		for _, port := range ports {
			fmt.Printf("Found port: %v\n", port)
		}
	}
}
