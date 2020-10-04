package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
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
var HOST = "3700.network"
var PORT = "21"
var ADDRESS = HOST + ":" + PORT
var PATH = "/"

// command line variables
var help_flag bool
var verbose_flag bool
var op string
var param1 string
var param2 string
var file = ""

// command message to send to data channel
var msg string

// second command for mv
var msg2 string
var DATAADDR string

func initProgram() {
	helpFlag := flag.Bool("help", false, "show this help message and exit")
	verboseFlag := flag.Bool("verbose", false, "print all messages to and from the FTP server")
	flag.Parse()

	if *helpFlag {
		initHelp()
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
			// checks if either parameter is a url or file
			param1, erru1 := url.Parse(os.Args[2])
			// parse url to copy file from remote to local
			if param1.Scheme != "" {
				SCHEME = param1.Scheme
				USER = param1.User.Username()
				p, _ := param1.User.Password()
				PASS = p
				PATH = param1.Path
				file = os.Args[3]
				msg = "RETR " + PATH + "\r\n"
			}

			param2, erru2 := url.Parse(os.Args[3])
			// parse url to copy file from local to remote
			if param2.Scheme != "" {
				SCHEME = param2.Scheme
				USER = param2.User.Username()
				p, _ := param2.User.Password()
				PASS = p
				PATH = param2.Path
				file = os.Args[2]
				msg = "STOR " + PATH + "\r\n"
			}

			if erru1 != nil || erru2 != nil {
				fmt.Println("Failed to parse through URL.")
				os.Exit(1)
			}

			if op == "mv" {
				// copy file, then delete
				msg = "STOR " + PATH + "\r\n"
				msg2 = "DELE " + PATH + "\r\n"
				fmt.Println(msg)
			}
		} else {
			rawUrl := os.Args[2]
			// verify correct URL format
			u, err := url.Parse(rawUrl)
			if err != nil {
				panic(err)
			}
			fmt.Println(u)
			// required parameters: HOST and PATH
			SCHEME = u.Scheme
			USER = u.User.Username()
			p, _ := u.User.Password()
			PASS = p

			// TODO: set default port or change if provided
			ADDRESS = u.Host + ":" + PORT
			PATH = u.Path
			//host, port, _ := net.SplitHostPort(u.Host)
			//fmt.Println(host)
			//fmt.Println(port)

			switch op {
			// requires URL
			case "ls":
				msg = "LIST " + PATH + "\r\n"
			case "mkdir":
				msg = "MKD " + PATH + "\r\n"
			case "rm":
				msg = "DELE " + PATH + "\r\n"
			case "rmdir":
				msg = "RMD " + PATH + "\r\n"
			default:
				fmt.Println("This command is not supported. Use -h or -help to see proper usage.")
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
	fmt.Println("Open control channel")
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

	// SETUP
	processMessage(conn, username)
	if PASS != "" {
		processMessage(conn, password)
	}
	processMessage(conn, binaryType)
	processMessage(conn, streamMode)
	processMessage(conn, fileMode)
	processMessage(conn, msg)
}

// sends message to server from control channel
func processMessage(conn net.Conn, message string) {
	fmt.Println(message)
	open := "PASV\r\n"
	code := strings.Split(strings.TrimRight(message, "\r\n"), " ")[0]

	// open data channel
	if code == "LIST" || code == "STOR" || code == "RETR" {
		processMessage(conn, open)
		if code == "STOR" {
			fmt.Println("Uploading data...")
			go sendData(file, DATAADDR)
		}

		if code == "RETR" || code == "LIST" {
			fmt.Println("Downloading data...")
			go processData(DATAADDR)
		}
	}

	// writes message to server
	_, writeErr := conn.Write([]byte(message))
	// reads response message from server
	result := make([]byte, 1024)
	for {
		n, readErr := bufio.NewReader(conn).Read(result)
		if readErr != nil {
			panic(readErr)
		} else {
			fmt.Println(">> ", string(result[4:n]))
			break
		}
	}

	if writeErr != nil {
		log.Fatal("Something went wrong!")
		os.Exit(1)
	}

	// return IP address and port numbers to create data channel
	if code == "PASV" {
		// parse through ip addresses (first four) and port numbers (last two)
		nums := regexp.MustCompile(`\((.*?)\)`)
		parsedNums := strings.Trim(nums.FindAllString(string(result), -1)[0], "()")
		parsed := strings.Split(parsedNums, ",")
		ipNum, errNum := strconv.Atoi(parsed[len(parsed)-2])
		ipNum2, errNum2 := strconv.Atoi(parsed[len(parsed)-1])

		if errNum != nil || errNum2 != nil {
			log.Fatal("Parsing is incorrect.")
			os.Exit(1)
		}

		IP := strings.Join(parsed[:len(parsed)-2], ".")
		DATAPORT := strconv.Itoa(ipNum<<8 + ipNum2)
		DATAADDR = IP + ":" + DATAPORT
	}
}

// download data via data channel
func processData(address string) {
	fmt.Println(msg)
	code := strings.Split(strings.TrimRight(msg, "\r\n"), " ")[0]

	// create TCP client and connects to network server
	data, err := net.Dial("tcp", address)
	if err != nil {
		fmt.Println("Connection to data channel went wrong.")
		return
	}

	// reads response message from server
	result := make([]byte, 2048)
	n, readErr := bufio.NewReader(data).Read(result)
	if readErr != nil {
		if readErr == io.EOF {
			fmt.Println("No data.")
			return
		}
		panic(readErr)
	} else {
		if code == "RETR" {
			fmt.Println(PATH)
			source, sourceErr := os.Open(PATH)
			if sourceErr != nil {
				return
			}
			// create local file
			fmt.Println("I reached here")
			filepath, outErr := os.Create(file)
			if outErr != nil {
				panic(outErr)
			}
			fmt.Println("ASDJKJSK ", filepath)
			//defer filepath.Close()
			_, dataErr := io.Copy(filepath, source)
			if dataErr != nil {
				panic(dataErr)
			}
			fmt.Println("Finished downloading.")
		} else {
			fmt.Println("--------------------------------------------------------------------------------")
			fmt.Println(string(result[:n]))
			fmt.Println("--------------------------------------------------------------------------------")

		}
	}
	fmt.Println("Data received!")
}

// upload data via data channel
func sendData(file string, address string) {
	fileBytes, err := os.Open(file)

	// create TCP client and connects to network server
	data, err := net.Dial("tcp", address)
	if err != nil {
		fmt.Println("Connection to data channel went wrong.")
		return
	}

	// sends the file data to the server
	fileData, writeErr := io.Copy(data, fileBytes)
	fmt.Println("NUM OF BYTES: ", fileData)
	if writeErr != nil {
		fmt.Println("Error with sending file data.")
		panic(writeErr)
	}
	defer data.Close()
	fmt.Println("Data uploaded!")
}

// help commands for ftp client usage
func initHelp() {
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

// build binary: go build 3700ftp.go
// ./3700ftp [operation] param1 [param2]
func main() {
	// initialize program and accept command line arguments
	initProgram()
	// open connection and send message to establish both socket connections
	openConnection()
}
