package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	"net/url"
	"os"
	"regexp"
	"strconv"
	"strings"
)

// URL variables with default values
var SCHEME = "ftp"
var USER = "anonymous"
var PASS = ""
var ADDRESS = "3700.network:21"
var PATH string

// command line variables
var help_flag bool
var verbose_flag bool
var op string
var param1 string
var param2 string

func initProgram() {
	helpFlag := flag.Bool("help", false, "show this help message and exit")
	verboseFlag := flag.Bool("verbose", false, "print all messages to and from the FTP server")
	flag.Parse()

	if *helpFlag {
		if len(os.Args[1:]) > 1 {
			op := os.Args[2]
			switch op {
			case "ls":
				fmt.Println("USAGE")
				fmt.Println("     ls <URL>")
				fmt.Println("Print out the directory listing from the FTP server at the given URL")
			case "mkdir":
				fmt.Println("USAGE")
				fmt.Println("     mkdir <URL>")
				fmt.Println("Create a new directory on the FTP server at the given URL")
			case "rm":
				fmt.Println("USAGE:")
				fmt.Println("     mkdir <URL>")
				fmt.Println("Delete the file on the FTP server at the given URL")
			case "rmdir":
				fmt.Println("USAGE:")
				fmt.Println("     rm <URL>")
				fmt.Println("Delete the directory on the FTP server at the given URL")
			case "cp":
				fmt.Println("USAGE:")
				fmt.Println("     cp <ARG1> <ARG2>")
				fmt.Println("Copy the file given by ARG1 to the file given by ARG2")
			case "mv":
				fmt.Println("USAGE:")
				fmt.Println("     mv <ARG1> <ARG2>")
				fmt.Println("Move the file given by ARG1 to the file given by ARG2")
			default:
				fmt.Println("You entered a command that doesn't exist.")
			}
		} else {
			fmt.Println("This FTP client supports the following operations:")
			fmt.Println("  ls <URL>                 Print out the directory listing from the FTP server at the given URL")
			fmt.Println("  mkdir <URL>              Create a new directory on the FTP server at the given URL")
			fmt.Println("  rm <URL>                 Delete the file on the FTP server at the given URL")
			fmt.Println("  rmdir <URL>              Delete the directory on the FTP server at the given URL")
			fmt.Println("  cp <ARG1> <ARG2>         Copy the file given by ARG1 to the file given by\n                           ARG2. If ARG1 is a local file, then ARG2 must be a URL, and vice-versa.")
			fmt.Println("  mv <ARG1> <ARG2>         Move the file given by ARG1 to the file given by\n                           ARG2. If ARG1 is a local file, then ARG2 must be a URL, and vice-versa.")
		}

	}

	if *verboseFlag {
		// print out all messages to and from FTP server
		fmt.Println(*verboseFlag)
	}

	if !*helpFlag && !*verboseFlag {
		if len(os.Args[1:]) == 1 {
			fmt.Println("Usage: ./3700ftp [operation] param1 [param2]")
			os.Exit(1)
		}

		op := os.Args[1]
		if op == "cp" || op == "mv" {
			// requires two arguments
			// arg1 = file/URL
			// arg2 = URL/file
			param1 := os.Args[2]
			param2 := os.Args[3]
			fmt.Println(param1)
			fmt.Println(param2)
		} else {
			rawUrl := os.Args[2]
			// verify correct URL format
			u, err := url.Parse(rawUrl)
			if err != nil {
				log.Println(err)
			}
			fmt.Println(u)
			// required parameters: HOST and PATH
			SCHEME = u.Scheme
			USER = u.User.Username()
			p, _ := u.User.Password()
			PASS = p
			ADDRESS = u.Host
			PATH = u.Path
			//host, port, _ := net.SplitHostPort(u.Host)
			//fmt.Println(host)
			//fmt.Println(port)

			switch op {
			// requires URL
			case "ls":
			case "mkdir":
			case "rm":
			case "rmdir":
			default:
				fmt.Println("This command is not supported. Use -h or -help to ")
				os.Exit(1)
			}
		}

		fmt.Println("FTP client for listing, copying, moving, and deleting files and directories on remote FTP servers.")
		// --verbose, -v
		// --help, -h
	}
}

// establish TCP control channel and send commands
func openConnection() {
	fmt.Println(ADDRESS)
	// create TCP client and connects to network server
	conn, err := net.Dial("tcp", ADDRESS)

	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Success!")
	// client settings
	username := "USER " + USER + "\r\n"
	password := "PASS " + PASS + "\r\n"
	binaryType := "TYPE " + "I\r\n"
	streamMode := "MODE " + "S\r\n"
	fileMode := "STRU " + "F\r\n"
	open := "PASV\r\n"

	// SETUP
	processMessage(conn, username)
	if PASS != "" {
		processMessage(conn, password)
	}
	processMessage(conn, binaryType)
	processMessage(conn, streamMode)
	processMessage(conn, fileMode)
	// open data channel
	processMessage(conn, open)
}

// sends message to server
func processMessage(conn net.Conn, message string) {
	fmt.Println(strings.TrimRight(message, "\r\n"))
	// writes message to server
	_, writeErr := conn.Write([]byte(message))
	result := make([]byte, 128)
	// reads response message from server
	_, readErr := conn.Read(result)
	fmt.Println(">> ", string(result))

	// return IP address and port numbers to create data channel
	if strings.TrimRight(message, "\r\n") == "PASV" {
		nums := regexp.MustCompile(`\((.*?)\)`)
		// parse through ip addresses (first four) and port numbers (last two)
		parsedNums := strings.Trim(nums.FindAllString(string(result), -1)[0], "()")
		parsed := strings.Split(parsedNums, ",")
		ipNum, errNum := strconv.Atoi(parsed[len(parsed) - 2])
		ipNum2, errNum2 := strconv.Atoi(parsed[len(parsed) - 1])

		if errNum != nil || errNum2 != nil {
			log.Fatal("Parsing is incorrect.")
			os.Exit(1)
		}

		IP := strings.Join(parsed[:len(parsed) - 2], ".")
		DATAPORT := strconv.Itoa(ipNum << 8 + ipNum2)
		DATAADDR := IP + ":" + DATAPORT
		fmt.Println(DATAADDR)

		// TODO: get some responses!
		// create TCP client and connects to network server
		data, err := net.Dial("tcp", DATAADDR)
		fmt.Println(data)
		_, dataErr := data.Read(result)
		fmt.Println(">> ", string(result))

		processMessage(data, "")

		if err != nil || dataErr != nil {
			fmt.Println(err)
			return
		}
	}

	if writeErr != nil || readErr != nil {
		log.Fatal("Something went wrong!")
		os.Exit(1)
	}
}

// download or upload data with commands via data channel
func processData() {
	//for {
		// data commands
		//list := "LIST " + "\r\n"
		//delete := "DELE " + "\r\n"
		//makeDir := "MKD " + "\r\n"
		//removeDir := "RMD " + "\r\n"
		//upload := "STOR " + "\r\n"
		//download := "RETR " + "\r\n"
		//quit := "QUIT\r\n"

		//reader := bufio.NewReader(conn)
		//if err != nil {
		//	log.Fatal("Something went wrong: ", err)
		//	return
		//}
	//}

	//conn.Close()
}

// build binary: go build 3700ftp.go
// ./3700ftp [operation] param1 [param2]
func main() {
	initProgram()
	openConnection()
}
