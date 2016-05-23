#include <iostream>
#include <cstdio>
#include <cstdint>
#include <cstring>
using namespace std;

uint32_t find_incdseq(uint32_t const sequence[], int const& N, int const& K, int64_t const& incdseq_count_mod);

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
  int64_t const incdseq_count_mod = 5000000;

  uint32_t total_incdseq_count = find_incdseq(sequence, N, K, incdseq_count_mod);

  printf("%u\n", total_incdseq_count);

  return 0;
}

uint32_t find_incdseq(uint32_t const sequence[], int const& N, int const& K, int64_t const& incdseq_count_mod) {
  // number of distinct increasing subsequences
  //   for the sequence starting from index i,
  //   of length j, is incdseq_count[i][j]
  int64_t incdseq_count[N+1][K+1];
  memset(incdseq_count, 0, sizeof(incdseq_count[0][0])*(N+1)*(K+1));
  
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
      incdseq_count[N_iter][K_iter] = incdseq_count[N_iter+1][K_iter];

      // if the number at the current index is to be included
      if (K_iter == 1) {
        incdseq_count[N_iter][K_iter]++;
        for (int32_t i=N_iter+1 ; i<=N-1 ; i++) {
          if (sequence[i] == sequence[N_iter]) {
            incdseq_count[N_iter][K_iter]--;
            break;
          }
        }
      } else {
        for (int32_t i=N_iter+1 ; i<=N-K_iter+1 ; i++) {
          if ( (sequence[i] > sequence[N_iter]) && (incdseq_count[i][K_iter-1] > incdseq_count[i+1][K_iter-1]) ) {
            incdseq_count[N_iter][K_iter] += (incdseq_count[i][K_iter-1] - incdseq_count[i+1][K_iter-1]);
            incdseq_count[N_iter][K_iter] = ( (incdseq_count[N_iter][K_iter] % incdseq_count_mod) + incdseq_count_mod ) % incdseq_count_mod;
          } else if (sequence[i] == sequence[N_iter]) {
            break;
          }
        }
      }

      incdseq_count[N_iter][K_iter] = ( (incdseq_count[N_iter][K_iter] % incdseq_count_mod) + incdseq_count_mod ) % incdseq_count_mod;

      // done
    }
  }

  // for debug
  bool debug_table = true;
  if (debug_table) {
    printf("N = %d, K = %d\n\n", N, K);

    printf("    ");
    for (int i=0; i<N; i++) {
      printf("%4u", sequence[i]);
    }
    printf("\n\n");

    printf("    ");
    for (int i=0; i<N; i++) {
      printf("%4d", i);
    }
    printf("\n");

    printf("    ");
    for (int i=0; i<N; i++) {
      printf("----");
    }
    printf("\n");

    for (int j=1; j<=K; j++) {
      printf("%4d", j);
      for (int i=0; i<N; i++) {
        printf("%4ld", incdseq_count[i][j]);
      }
      printf("\n");
    }
  }

  return (uint32_t)incdseq_count[0][K];
}
