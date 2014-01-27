package main

import  "fmt"

func swap(x, y string) (string, string) {
    return y , x
}

func main() {

    x, y := swap("hi", "hello")

    fmt.Println(x, y)

}
