package main

import (
    "fmt"
    "time"
)

func hello(s string) {
    for i := 0 ; i < 10 ; i++ {
        time.Sleep(1000 * time.Millisecond)
        fmt.Println(s)
    }

}

func main() {
    go hello("Hi")
    hello("Hello")

}
