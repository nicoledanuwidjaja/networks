package main

import (
    "flag"
    "fmt"
    "os"
)

var help_flag bool
var verbose_flag bool
var op string
var param1 string
var param2 string

func initProgram() {
    if len(os.Args[1:]) == 1 {
        fmt.Println("Usage: ./3700ftp [operation] param1 [param2]")
        os.Exit(1)
    }

    op := os.Args[1]
    param1 := os.Args[2]
    param2 := os.Args[3]

    help_flag := flag.Bool("help", false, "show this help message and exit")
    verbose_flag := flag.Bool("verbose", false, "print all messages to and from the FTP server")
    flag.Parse()

    if *help_flag {
        fmt.Println(*help_flag)
    }

    if *verbose_flag {
        fmt.Println(*verbose_flag)
    }

    switch op {
    // requires URL
    case "ls":
    case "mkdir":
    case "rm":
    case "rmdir":
    // requires two arguments
    // arg1 = file/URL
    // arg2 = URL/file
    case "cp":
    case "mv":
    default:
        fmt.Println("Something special here")
    }

    fmt.Println(op)
    fmt.Println(param1)
    fmt.Println(param2)

    fmt.Println("FTP client for listing, copying, moving, and deleting files and directories on remote FTP servers.")
    // --verbose, -v
    // --help, -h

    fmt.Println("ftp://[USER[:PASSWORD]@]HOST[:PORT]/PATH")
    // HOST = domain name/IP address
    // PORT = 21
    // USER = 'anonymous'
    // PASSWORD = ''
}

// build binary: go build 3700ftp.go
// ./3700ftp [operation] param1 [param2]
func main() {
    initProgram()
}

