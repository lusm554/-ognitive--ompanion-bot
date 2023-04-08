#!/bin/bash

grep -rnw $1 -e $2 | sort | bat
