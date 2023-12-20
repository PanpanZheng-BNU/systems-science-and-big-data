#include "myfuncs.c"

int main(int argc, char *argv[]) {
  int m, n, p;
  char *output;
  /*double start_time, end_time, t1, t2;*/
  m = (int)strtol(argv[1], &output, 10);
  n = (int)strtol(argv[2], &output, 10);
  p = (int)strtol(argv[3], &output, 10);

  int m1[m][n];
  int m2[n][p];
  int result_single[m][p];
  int result_multi[m][p];

  gen_mat(m, n, m1);
  gen_mat(n, p, m2);

  single_multiplication(m, n, p, m1, m2, result_single);
  multi_multiplication(m, n, p, m1, m2, result_multi);

  write_csv(m,n,m1, "m1.csv");
  write_csv(n,p,m2, "m2.csv");
  write_csv(m,p,result_single, "result-single.csv");
  write_csv(m,p,result_multi, "result-multi.csv");

  return 0;
}
