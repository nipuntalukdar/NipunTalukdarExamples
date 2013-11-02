package main

import "fmt"

func fibonacci(c chan uint64, max int) {
    start := 0
    startfib := uint64(0)
    startfib2 := uint64(1)
    temp := uint64(0)
    for ;start < max ; start++ {
        c <- startfib
        temp = startfib
        startfib = startfib2
        startfib2 = temp + startfib
    }
    close(c)
}

func main() {
    
    c := make(chan uint64, 100)
    go fibonacci(c, 50)
    for i:= range c {
        fmt.Println(i)
    }
}
