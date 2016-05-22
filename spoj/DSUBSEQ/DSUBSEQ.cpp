#include <iostream>
#include <cstdint>
#include <cstring>
using namespace std;

uint32_t find_dsubseq(char const sequence[], int const& size, uint32_t const& dsubseq_count_mod);

int main(int argc, char *argv[]) {
  // T : number of testcases (strings)
  //     1 <= T <= 100
  int T;
  scanf("%d", &T);

  int const max_len = 100001;
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

uint32_t find_dsubseq(char const sequence[], int const& size, uint32_t const& dsubseq_count_mod) {
  // dsubseq_count[ starting from index i ][ subsequence of length j ]
  int64_t dsubseq_count[size+1];
  memset(dsubseq_count, 0, sizeof(dsubseq_count[0])*(size+1));

  // 26 alphabets
  int last_seen[26];
  for (int i=0; i<26; i++) {
    last_seen[i] = -1;
  }

  // the empty subsequence
  dsubseq_count[size] = 1;

  for (int i=size-1; i>=0; i--) {
    dsubseq_count[i] = dsubseq_count[i+1];

    int last_seen_char = last_seen[ int(sequence[i]-'A') ];

    if (last_seen_char > i) {
      dsubseq_count[i] += (dsubseq_count[i+1] - dsubseq_count[last_seen_char+1]);
      dsubseq_count[i] = ( (dsubseq_count[i] % dsubseq_count_mod) + dsubseq_count_mod ) % dsubseq_count_mod;
    } else {
      dsubseq_count[i] += dsubseq_count[i+1];
      dsubseq_count[i] = ( (dsubseq_count[i] % dsubseq_count_mod) + dsubseq_count_mod ) % dsubseq_count_mod;
    }

    last_seen[ int(sequence[i]-'A') ] = i;
  }

  dsubseq_count[0] = ( (dsubseq_count[0] % dsubseq_count_mod) + dsubseq_count_mod ) % dsubseq_count_mod;

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

    printf("    ");
    for (int j=0; j<size; j++) {
      printf("%4ld", dsubseq_count[j]);
    }
    printf("\n");
  }

  return (uint32_t)dsubseq_count[0];
}
