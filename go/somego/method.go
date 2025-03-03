package main
import "fmt"

type  Vertex struct {
    x int
    y int

}

func (v *Vertex) show() {
    fmt.Println(v.x, v.y)

}

func main() {
    a := Vertex{1, 2}
    a.show()
}
