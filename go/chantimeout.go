package main

import (
	"fmt"
	"time"
)

func main() {
	c := make(chan int, 60)
	i := 0
	go func(ci chan int) {
		for {
			x := <-ci
			fmt.Println(x)
			time.Sleep(4 * time.Second)
		}
	}(c)

	t := time.NewTicker(1 * time.Second)
	for ; i < 3100000; i++ {
		for {
			select {
			case c <- i:
				fmt.Printf("Pushed %d\n", i)
				break
			case <-t.C:
				fmt.Println("Got timed out")
				continue
			}
		}
	}
	fmt.Printf("Down %d\n", cap(c))
}
