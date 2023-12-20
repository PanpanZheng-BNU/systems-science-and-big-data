#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

void gen_mat(int r, int c, int mat[r][c]) {
  for (int i = 0; i < r; i++) {
    for (int j = 0; j < c; j++) {
      mat[i][j] = rand() % 5;
    }
  }
}

void show_mat(int r, int c, int mat[r][c]) {
  for (int i = 0; i < r; i++) {
    for (int j = 0; j < c; j++) {
      printf("\t%d", mat[i][j]);
    }
    printf("\n");
  }
  return;
}

void single_multiplication(int m, int n, int p, int m1[m][n], int m2[n][p],
                           int result[m][p]) {
  for (int i = 0; i < m; i++) {
    for (int j = 0; j < p; j++) {
      result[i][j] = 0;

      for (int k = 0; k < n; k++) {
        result[i][j] += m1[i][k] * m2[k][j];
      }
    }
  }
}

void multi_multiplication(int m, int n, int p, int m1[m][n], int m2[n][p],
                          int result[m][p]) {
  int i, j, k;
#pragma omp parallel for private(i, j, k) shared(m1, m2, result)
  for (i = 0; i < m; i++) {
    for (j = 0; j < p; j++) {
      result[i][j] = 0;
      for (k = 0; k < n; k++) {
        result[i][j] += m1[i][k] * m2[k][j];
      }
    }
  }
}

void write_csv(int row, int col, int matrix[row][col], char str[]) {
  FILE *fpt;
  fpt = fopen(str, "w+");
  for (int i = 0; i < row; i++) {
    for (int j = 0; j < col; j++) {
      if (j == col - 1)
        fprintf(fpt, "%d\n", matrix[i][j]);
      else
        fprintf(fpt, "%d,", matrix[i][j]);
    }
  }
  fclose(fpt);
}
