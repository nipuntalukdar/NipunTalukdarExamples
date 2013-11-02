package main
import
(
    "fmt"
    "math"
)

type Abser interface {
    Abs() float64
}

type MyFloat float64

func (v* MyFloat) Abs() float64 {
    if *v < 0.0 {
        return float64(-*v)
    }

    return float64(*v)

}
/*
func (v MyFloat) Abs() float64 {
    if v < 0.0 {
        return float64(-v)
    }

    return float64(v)

} */

func main() {
    var a Abser
    f:= MyFloat(-math.Sqrt(3))
    a = &f
    fmt.Println(a.Abs())

}
