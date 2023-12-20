#!$HOME/julia-1.9.3/bin/julia

using CSV, DataFrames

m1 = Matrix(CSV.read("./m1.csv", DataFrame, header=false))
m2 = Matrix(CSV.read("./m2.csv", DataFrame, header=false))
result1 = Matrix(CSV.read("./result-single.csv", DataFrame, header=false))
result2 = Matrix(CSV.read("./result-multi.csv", DataFrame, header=false))
println("the result of single thread is: " * string(m1 * m2 == result1))
println("the result of multi thread is: " * string(m1 * m2 == result2))
println("the size of m1 is " * string(size(m1)))
println("the size of m2 is " * string(size(m2)))
println("the size of result is " * string(size(result1)))
