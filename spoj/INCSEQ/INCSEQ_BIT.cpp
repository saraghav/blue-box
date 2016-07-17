#include <iostream>
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <vector>
using namespace std;

// Assumptions:
// Data is processed sequentially while constructing the binary indexed tree
// All the values (frequencies) are integers
class BinaryIndexedTree {
private:
  vector<int64_t> tree;
  int64_t const value_mod;
  int64_t const max_index;

public:
  BinaryIndexedTree(int64_t const& max_index, int64_t const& value_mod) : tree(max_index, 0), value_mod(value_mod), max_index(max_index) {
  }

  void update_add(int64_t index, int64_t value_delta) {
    while (value_delta >= value_mod) {
      value_delta -= value_mod;
    }

    while (index < max_index) {
      tree[index] += value_delta;
      while (tree[index] >= value_mod) {
        tree[index] -= value_mod;
      }
      index += (index & -index);
    }
  }

  int64_t query(int64_t index) {
    int64_t cumulative_sum = 0;
    while (index > 0) {
      cumulative_sum += tree[index];
      while (cumulative_sum >= value_mod) {
        cumulative_sum -= value_mod;
      }
      index -= (index & -index);
    }
    return cumulative_sum;
  }
};

uint32_t find_incseq(uint32_t const sequence[], int32_t const& N, int32_t const& K, int64_t const& incseq_max_val, int64_t const& incseq_count_mod);

int main(int argc, char *argv[]) {
  // N : length of input sequence
  // K : length of increasing subsequence being searched
  int32_t N, K;
  scanf("%d %d", &N, &K);

  // the input sequence of numbers
  uint32_t sequence[N];
  for (uint32_t *element = sequence; element <= &sequence[N-1]; element++) {
    scanf("%u", element);
    (*element)++; // to avoid zero for use with BIT
  }
  int64_t const incseq_count_mod = 5000000;
  int64_t const incseq_max_val = 100000;
  uint32_t total_incseq_count = find_incseq(sequence, N, K, incseq_max_val, incseq_count_mod);

  printf("%u", total_incseq_count);

  return 0;
}

uint32_t find_incseq(uint32_t const sequence[], int32_t const& N, int32_t const& K, int64_t const& incseq_max_val, int64_t const& incseq_count_mod) {
  vector<BinaryIndexedTree> BIT(K+1, BinaryIndexedTree(incseq_max_val+1, incseq_count_mod));

  for (int32_t N_iter=0; N_iter<N; N_iter++) {
    BIT[1].update_add(sequence[N_iter], 1);
    for (int32_t K_iter=2; K_iter<=K; K_iter++) {
      BIT[K_iter].update_add(sequence[N_iter], BIT[K_iter-1].query(sequence[N_iter]-1));
    }
  }

  return BIT[K].query(incseq_max_val);
}
