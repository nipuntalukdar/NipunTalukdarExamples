package main

import (
    "fmt"
    "time"
)

func main() {
    tick:= time.Tick(100 * time.Millisecond)
    boom:= time.After(1000 * time.Millisecond)

    for  {
        select {
            case <- tick:
                fmt.Println("Tick")
            case <- boom:
                fmt.Println("Boomed")
                return
            default:
                fmt.Println("............")
                time.Sleep(10 * time.Millisecond)
        }
    }

}
