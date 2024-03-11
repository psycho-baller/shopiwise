package main

import (
	"log"
	"net/http"

	intentions "github.com/psycho-baller/shopiwise/intentions"
)
func logger(f http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("%s %s %s\n", r.RemoteAddr, r.Method, r.URL)
		f(w, r)
	}
}
func enableCors(f http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Origin", "chrome-extension://apooihdpamempipjkgbheiggadjjcoho")
		if r.Method == "OPTIONS" {
			w.Header().Set("Access-Control-Allow-Headers", "Content-Type")//, Accept, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
			return
		}
		f(w, r)
	}
}

func main() {
	http.HandleFunc("/api/intentions", logger(enableCors(intentions.Intentions)))
	
	http.ListenAndServe(":8000", nil)
}
