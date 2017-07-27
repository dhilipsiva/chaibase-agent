#! /bin/bash
#
# build_windows.sh
# Copyright (C) 2017 dhilipsiva <dhilipsiva@gmail.com>
#
# Distributed under terms of the MIT license.
#


GOOS=windows GOARCH=386 go build -o agent.exe agent.go
