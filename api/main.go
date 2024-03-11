package main

import (
	"log"
	"net/http"
)

func logger(f http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("%s %s %s\n", r.RemoteAddr, r.Method, r.URL)
		f(w, r)
	}
}
func main() {
	http.HandleFunc("/intentions", logger(Intentions))
	
	http.ListenAndServe(":80", nil)
}
