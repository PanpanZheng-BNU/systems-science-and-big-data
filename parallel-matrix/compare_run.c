#include "myfuncs.c"

int main(int argc, char *argv[]) {
  int m, n, p;
  char *output;
  double start_time, end_time, t1, t2;
  m = (int)strtol(argv[1], &output, 10);
  n = (int)strtol(argv[2], &output, 10);
  p = (int)strtol(argv[3], &output, 10);

  int m1[m][n];
  int m2[n][p];
  int result_single[m][p];
  int result_multi[m][p];

  gen_mat(m, n, m1);
  gen_mat(n, p, m2);

  start_time = omp_get_wtime();
  single_multiplication(m, n, p, m1, m2, result_single);
  end_time = omp_get_wtime();
  t1 = end_time - start_time;

  start_time = omp_get_wtime();
  multi_multiplication(m, n, p, m1, m2, result_multi);
  end_time = omp_get_wtime();
  t2 = end_time - start_time;


  printf("%d,%d,%d,%lf,%lf\n", m, n, p, t1, t2);

  return 0;
}
