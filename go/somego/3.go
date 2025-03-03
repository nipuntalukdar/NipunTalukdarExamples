package main
import (
    "fmt"
    "net"
    "os"
    "time"
    "math/rand"
)

func main() {
    fmt.Println("Welcome ")
    fmt.Println("Time is now ", time.Now())
    fmt.Println("Try opening a file ")
    fmt.Println(os.Open("a.txt"))
    fmt.Println("Or access the network")
    fmt.Println(net.Dial("tcp", "google.com:80"))
    fmt.Println("My random ", rand.Intn(10))

}
