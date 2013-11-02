package main

import (
    "fmt"  
    "time"
)

func readChan(c chan int ) {
    for {
        j := <- c
        fmt.Println(j)
    }

}

func main() {
    c := make (chan int, 2)

    j := 0
    go readChan(c)
    for i := 0 ; i < 2;  {
        time.Sleep(100 * time.Millisecond)
        c <-  j
        j += 2
        c <- j
        fmt.Println("Hi") 
    }
}
