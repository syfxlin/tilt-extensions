package main

import (
	"bufio"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"time"
)

func try(err error) {
	if err != nil {
		panic(err)
	}
}

func build(src *os.File, dist *os.File) {
	err := dist.Truncate(0)
	try(err)
	reader := bufio.NewScanner(src)
	writer := bufio.NewWriter(dist)
	for reader.Scan() {
		line := reader.Text()
		matched, err := regexp.MatchString("^\\s*(import|from)\\s+", line)
		try(err)
		if matched {
			continue
		}
		matched, err = regexp.MatchString("^\\s*# define\\s*$", line)
		try(err)
		if matched {
			break
		}
		_, err = writer.WriteString(line + "\n")
		try(err)
	}
	err = writer.Flush()
	try(err)
}

func watch(src *os.File, dist *os.File) {
	go func() {
		stat, err := os.Stat(src.Name())
		try(err)
		for {
			_stat, err := os.Stat(src.Name())
			try(err)
			if stat.Size() != _stat.Size() || stat.ModTime() != _stat.ModTime() {
				build(src, dist)
				stat = _stat
			}
			time.Sleep(1 * time.Second)
		}
	}()
}

func tilt(args []string) {
	cwd, err := os.Getwd()
	try(err)
	src, err := os.Open(filepath.Join(cwd, "Tiltfile.py"))
	try(err)
	defer src.Close()
	dist, err := os.OpenFile(filepath.Join(cwd, "Tiltfile"), os.O_WRONLY|os.O_CREATE, 0755)
	try(err)
	defer dist.Close()

	build(src, dist)
	watch(src, dist)

	args = append(args, "-f", dist.Name())
	cmd := exec.Command("tilt", args...)
	cmd.Dir = cwd
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err = cmd.Run()
	try(err)
}

func convert() {
	cwd, err := os.Getwd()
	try(err)
	src, err := os.Open(filepath.Join(cwd, "Tiltfile.py"))
	try(err)
	defer src.Close()
	dist, err := os.OpenFile(filepath.Join(cwd, "Tiltfile"), os.O_WRONLY|os.O_CREATE, 0755)
	try(err)
	defer dist.Close()

	build(src, dist)
}

func main() {
	args := os.Args[1:]
	if args[0] == "up" || args[0] == "down" || args[0] == "ci" {
		tilt(args)
	} else if args[0] == "convert" {
		convert()
	} else {
		panic("tilt-re only support subcommands in [up, down, ci, convert]")
	}
}
