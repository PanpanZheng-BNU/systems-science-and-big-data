#!/bin/zsh
gcc -fopenmp -o t3 ./results_csv_run.c

chmod +x ./t3

./t3 100 30 40

julia ./check_result.jl


