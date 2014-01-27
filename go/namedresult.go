package main
import "fmt"

func split(sum int) (x, y int) {
    x = sum -20
    y = sum -80
    return
}

func main() {
    x, y := split(100)
    fmt.Println(x,y)

    
}
