package main

import (
	"encoding/json"
	// "fmt"
	"net/http"
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
	http.HandleFunc("/", handler)
	http.ListenAndServe(":9876", nil)
}
