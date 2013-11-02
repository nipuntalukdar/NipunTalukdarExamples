package main 
import "fmt"

func fibonacci(c, quit chan int) {
    x, y := 0, 1
    for {
        select {
            case c <- x:
                x, y = y, x + y
            case <- quit:
                fmt.Println("Quiting")
                return
        }
    }
}

func main() {
    c := make(chan int)
    quit := make(chan int)
    go func() {
        for i:= 0; i < 100; i++ {
            fmt.Println("Starting")
            fmt.Println(<- c)
        }
        quit <- 0
    }()
    
    fibonacci(c, quit)
}
