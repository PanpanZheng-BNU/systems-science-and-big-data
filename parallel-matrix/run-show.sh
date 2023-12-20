#!/bin/zsh
gcc -fopenmp -o t2 ./show_run.c

chmod +x ./t2

./t2 3 4 5

