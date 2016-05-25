#include <iostream>
#include <cstdio>
#include <cstdint>
#include <cstring>
using namespace std;

uint32_t find_incseq(uint32_t const sequence[], int32_t const& N, int32_t const& K, int64_t const& incseq_count_mod);

int main(int argc, char *argv[]) {
  // N : length of input sequence
  // K : length of increasing subsequence being searched
  int32_t N, K;
  scanf("%d %d", &N, &K);

  // the input sequence of numbers
  uint32_t sequence[N];
  for (uint32_t *element = sequence; element <= &sequence[N-1]; element++) {
    scanf("%u", element);
  }
  int64_t const incseq_count_mod = 5000000;
  uint32_t total_incseq_count = find_incseq(sequence, N, K, incseq_count_mod);

  printf("%u", total_incseq_count);

  return 0;
}

uint32_t find_incseq(uint32_t const sequence[], int32_t const& N, int32_t const& K, int64_t const& incseq_count_mod) {
  // number of distinct increasing subsequences
  //   for the sequence starting from index i,
  //   of length j, is incseq_count[i][j]
  int64_t incseq_count[N+1][K+1];
  memset(incseq_count, 0, sizeof(incseq_count[0][0])*(N+1)*(K+1));

  for (int32_t K_iter=1 ; K_iter<=K ; K_iter++) {
    for (int32_t N_iter=N-1 ; N_iter>=0 ; N_iter--) {
      // if number of elements being considered is less
      //   than desired subsequence length
      if ( (N-N_iter) < K_iter ) {
        continue;
      }

      // if other case, use DP to compute the result
      
      // starting from the current index has at least the same number of
      //   length "K_iter" subsequences as starting from the next index
      //   (which means the subsequences don't contain the number at the
      //    current index)
      incseq_count[N_iter][K_iter] = incseq_count[N_iter+1][K_iter];

      // if the number at the current index is to be included
      if (K_iter == 1) {
        incseq_count[N_iter][K_iter]++;
      } else {
        for (int32_t i=N_iter+1 ; i<=N-K_iter+1 ; i++) {
          if ( (sequence[i] > sequence[N_iter]) && (incseq_count[i][K_iter-1] > incseq_count[i+1][K_iter-1]) ) {
            incseq_count[N_iter][K_iter] += (incseq_count[i][K_iter-1] - incseq_count[i+1][K_iter-1]);
            // incseq_count[N_iter][K_iter] = ( (incseq_count[N_iter][K_iter] % incseq_count_mod) + incseq_count_mod ) % incseq_count_mod;
            while ( incseq_count[N_iter][K_iter] >= incseq_count_mod ) {
              incseq_count[N_iter][K_iter] -= incseq_count_mod;
            }
          }
        }
      }

      // incseq_count[N_iter][K_iter] = ( (incseq_count[N_iter][K_iter] % incseq_count_mod) + incseq_count_mod ) % incseq_count_mod;
      while ( incseq_count[N_iter][K_iter] >= incseq_count_mod ) {
        incseq_count[N_iter][K_iter] -= incseq_count_mod;
      }

      // done
    }
  }

  // for debug
  bool debug_table = false;
  if (debug_table) {
    printf("N = %d, K = %d\n\n", N, K);

    printf("    ");
    for (int i=0; i<N; i++) {
      printf("%10u", sequence[i]);
    }
    printf("\n\n");

    printf("    ");
    for (int i=0; i<N; i++) {
      printf("%10d", i);
    }
    printf("\n");

    printf("    ");
    for (int i=0; i<N; i++) {
      printf("----");
    }
    printf("\n");

    for (int j=1; j<=K; j++) {
      printf("%10d", j);
      for (int i=0; i<N; i++) {
        printf("%10ld", incseq_count[i][j]);
      }
      printf("\n");
    }
  }

  return (uint32_t)incseq_count[0][K];
}
