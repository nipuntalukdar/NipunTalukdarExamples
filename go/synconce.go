package main
import (
    "fmt"
    "sync"
)

func main(){
    var once sync.Once
    onceBody := func() {
        fmt.Println("Only once")
    }
    done := make(chan bool)
    for i := 0; i < 10; i++ {
        go func() {
            once.Do(onceBody)
            done <- true
        }()
    }

    var x bool
    for i := 0 ; i < 10 ; i++ {
         x = <- done
         fmt.Printf("%v\n",x)
    }
}
