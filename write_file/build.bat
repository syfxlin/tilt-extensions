go build write_file.go

SET CGO_ENABLED=0
SET GOOS=linux
SET GOARCH=amd64
go build write_file.go