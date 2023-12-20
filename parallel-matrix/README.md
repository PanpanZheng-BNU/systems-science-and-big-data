# matrix multiplication
## `.c` 文件
- `myfuncs.c`：核心文件，存储矩阵乘法计算的函数 `single_multiplication()`（串行） `multi_multiplication()`（并行），生成矩阵的函数 `gen_mat()`，展示矩阵的函数 `show_mat()` 以及将矩阵写入 `.csv` 文件的函数 `write_csv()`。
    - `compare_run.c`：用于执行 `myfuncs.c` 并输出运算时间；
    - `results_csv_run.c`：用于执行 `myfuncs.c` 并将计算中的矩阵记录进 `.csv` 文件以进行检查；
    - `show_run.c`：用于执行 `myfuncs.c` 并显示被计算的矩阵以及计算结果；

## `.sh` 文件
- `run-compare.sh`：用于编译执行 `compare_run.c`；并将结果记录进 `change_m.csv`, `change_n.csv`, `change_p.csv` 三个文件中
- `run-check.sh`：用于编译并执行 `results_csv_run.c`；将结果记录进 `result-multi.csv`, `result-single.csv` 两个文件中，并使用 `julia` 脚本 `check_result.jl` 检查计算结果的正确性；
- `run-show.sh`：用于编译并执行 `show_run.c` 展示被计算的矩阵和计算结果；


## `.jl` 文件
- `check_result.jl`：用于检验计算结果是否正确。需要安装 `CSV` `DataFrames` 两个包。

## `.ipynb` 用于可视化，使用 [julia](https://julialang.org)
- `speed_visualization.ipynb`

