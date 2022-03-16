package main

import (
	"fmt"
	"io/ioutil"
	"os"
)

func main() {
	filename := os.Getenv("FILENAME")
	contents := os.Getenv("CONTENTS")
	if filename == "" {
		file, err := ioutil.TempFile("", "tilt-")
		if err != nil {
			panic(err)
		}
		_, err = file.WriteString(contents)
		if err != nil {
			panic(err)
		}
		fmt.Print(file.Name())
	} else {
		err := ioutil.WriteFile(filename, []byte(contents), 0755)
		if err != nil {
			panic(err)
		}
		fmt.Print(filename)
	}
}
