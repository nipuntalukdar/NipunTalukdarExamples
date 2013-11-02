package main
import 
    ("fmt" 
    "math"
    )

type MyFloat float64

func (f MyFloat) Abs() float64 {
    if f < 0 {
        return float64(-f)
    }

    return float64(f)
}

func main() {
    x := MyFloat(-math.Sqrt(2))
    fmt.Println(x.Abs())
}
