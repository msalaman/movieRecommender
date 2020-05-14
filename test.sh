#!/bin/bash

# number to run in parallel
N=3
# directory to export outputs to
DIR=test
# file to write the accuracy scores to
FILE=results

mkdir $DIR
cat test_users | xargs -L 1 -I "%" -P $N bash -c "./main.py % > $DIR/%"
grep -o -E "Accuracy: ([0-1]\.[0-9]*)" test/* | grep -o -E "([0-1]\.[0-9]*)" > $DIR/$FILE
