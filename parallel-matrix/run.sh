#!/bin/zsh
gcc -fopenmp -o t matrix_multiplication.c

echo "m,n,p,single,multi" > "change_m.csv"

times=($(seq 1 20 801)) 

for VARIABLE in $times
do
  for new in 1 2 3 4 5
  do
    ./t $VARIABLE 500 500 >> "change_m.csv"
  done
done

echo "m,n,p,single,multi" > "change_n.csv"
for VARIABLE in $times
do
  for new in 1 2 3 4 5
  do
    ./t  500 $VARIABLE 500 >> "change_n.csv"
  done
done

echo "m,n,p,single,multi" > "change_p.csv"
for VARIABLE in $times
do
  for new in 1 2 3 4 5
  do
    ./t  500 500 $VARIABLE  >> "change_p.csv"
  done
done
#echo "------\nsingle\t\t multi"
#for VARIABLE in 8 80 800
#do
  #./t 500 500 $VARIABLE 
#done

#echo "------\nsingle\t\t multi"
#for VARIABLE in 8 80 800
#do
  #./t $VARIABLE 500 500
#done

