#include <iostream>
#include <cstdint>
#include <cstring>
using namespace std;

uint32_t find_dsubseq(char const sequence[], int size, uint32_t const& dsubseq_count_mod);

int main(int argc, char *argv[]) {
  // T : number of testcases (strings)
  //     1 <= T <= 100
  int T;
  scanf("%d", &T);

  int const max_len = 100000;
  uint32_t const dsubseq_count_mod = 1000000007;

  char testcase[max_len];
  int size = max_len;
  uint32_t dsubseq = 0;
  for (int i=0; i<T; i++) {
    scanf("%s", testcase);
    size = strlen(testcase);
    dsubseq = find_dsubseq(testcase, size, dsubseq_count_mod);

    printf("%u\n", dsubseq);
  }

  return 0;
}

uint32_t find_dsubseq(char const sequence[], int size, uint32_t const& dsubseq_count_mod) {
  // dsubseq_count[ starting from index i ][ subsequence of length j ]
  uint32_t dsubseq_count[size+1][size+1];
  memset(dsubseq_count, 0, sizeof(dsubseq_count[0][0])*(size+1)*(size+1));

  for (int i=size-1; i>=0; i--) {
    for (int j=0; j<=size; j++) {
      // the empty subsequence
      if (j == 0) {
        dsubseq_count[i][j] = 1;
        continue;
      }

      // the impossible subsequence
      //   when the number of available characters
      //   is less than the desired subsequence length
      if ( (size-i+1) < j ) {
        continue;
      }

      dsubseq_count[i][j] = dsubseq_count[i+1][j];
      if (j == 1) {
        dsubseq_count[i][j]++;
        for (int k=i+1; k<=size-1; k++) {
          if (sequence[k] == sequence[i]) {
            dsubseq_count[i][j]--;
            break;
          }
        }
      } else {
        for (int k=i+1; k<=size-1; k++) {
          dsubseq_count[i][j] += (dsubseq_count[k][j-1] - dsubseq_count[k+1][j-1]);
          dsubseq_count[i][j] %= dsubseq_count_mod;
          if (sequence[k] == sequence[i]) {
            break;
          }
        }
      }

      dsubseq_count[i][j] %= dsubseq_count_mod;
    }
  }

  uint32_t total_dsubseq_count = 0;
  for (int j=0; j<=size; j++) {
    total_dsubseq_count += dsubseq_count[0][j];
    total_dsubseq_count %= dsubseq_count_mod;
  }

  // for debug
  bool debug_table = false;
  if (debug_table) {
    printf("    ");
    for (int i=0; i<size; i++) {
      printf("%4c", sequence[i]);
    }
    printf("\n\n");

    printf("    ");
    for (int i=0; i<size; i++) {
      printf("%4d", i);
    }
    printf("\n");

    printf("    ");
    for (int i=0; i<size; i++) {
      printf("----");
    }
    printf("\n");

    for (int j=0; j<=size; j++) {
      printf("%4d", j);
      for (int i=0; i<size; i++) {
        printf("%4u", dsubseq_count[i][j]);
      }
      printf("\n");
    }
  }
  
  return total_dsubseq_count;
}
