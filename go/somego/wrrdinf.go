package main 

import (
    "fmt"
    "os"
)

type Read interface{
    Read(b []byte) (n int, err error)
}

type Write  interface {
    Write(b []byte) (n int, err error)
}

type RW interface {
    Write
    Read
}

func main(){
    var w Write
    w = os.Stdout
    fmt.Fprintf(w, "Hi Hello\n")
}
