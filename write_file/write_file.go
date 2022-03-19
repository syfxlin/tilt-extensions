package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"path/filepath"
	"strconv"
	"time"
)

func FindRootDir() (string, error) {
	curr, err := os.Executable()
	if err != nil {
		return "", err
	}
	prev := curr
	curr = filepath.Dir(curr)
	for curr != prev {
		if _, err := os.Stat(filepath.Join(curr, "tilt_modules")); !os.IsNotExist(err) {
			curr = filepath.Join(curr, ".temp")
			err := os.MkdirAll(curr, 0755)
			if err != nil {
				return "", err
			}
			return curr, nil
		}
		prev = curr
		curr = filepath.Dir(curr)
	}
	return "", errors.New("could not find tilt root dir")
}

func DeleteOldTempFiles(root string) error {
	files, err := ioutil.ReadDir(root)
	if err != nil {
		return err
	}
	for _, file := range files {
		if file.ModTime().Before(time.Now().Add(-12 * time.Hour)) {
			err := os.Remove(file.Name())
			if err != nil {
				return err
			}
		}
	}
	return nil
}

func main() {
	root := os.Getenv("ROOT_DIR")
	if root == "" {
		r, err := FindRootDir()
		if err != nil {
			panic(err)
		}
		root = r
	}
	err := DeleteOldTempFiles(root)
	if err != nil {
		panic(err)
	}

	filename := os.Getenv("FILENAME")
	contents := os.Getenv("CONTENTS")

	if filename == "" {
		r := rand.New(rand.NewSource(time.Now().UnixNano()))
		filename = filepath.Join(root, strconv.Itoa(r.Int()))
	}

	err = ioutil.WriteFile(filename, []byte(contents), 0755)
	if err != nil {
		panic(err)
	}
	fmt.Print(filename)
}
