package main

import (
    "fmt"
)

func  sum(a []int, c chan int){
    sum:= 0
    for _, v := range a {
        sum += v
    }

    c <- sum
}


func main() {
    c:= make(chan int)
    a:= [100000] int{}
    for i:= 0 ; i < 100000 ; i++ {
        a[i] = i * i
    }
    go sum(a[:len(a)/2], c)
    go sum(a[len(a)/2:],c)
    go sum(a[:], c)
    x,y,z := <- c , <- c , <-c
    fmt.Printf("Sum is %d, part sum %d and %d\n",
            z , x, y)

    
}
