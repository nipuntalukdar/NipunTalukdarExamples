package main
import (
    "fmt"
    "net/http"
    "time"
)

type Hello struct{}

func (h Hello) ServeHTTP( w http.ResponseWriter, r *http.Request) {
    fmt.Println("Got the request ", r)
    var x = fmt.Sprintf("Time now is %v\n", time.Now())
    fmt.Fprint(w, x)
}

func main() {
    fmt.Println("Hi")
    var h Hello
    http.ListenAndServe("localhost:4000", h)
}
