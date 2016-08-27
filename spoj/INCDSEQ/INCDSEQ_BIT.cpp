/*
 * SPOJ: Distinct Increasing Subsequences
 * http://www.spoj.com/problems/INCDSEQ/
 */

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
    while (value_delta < 0) {
      value_delta += value_mod;
    }
    while (value_delta >= value_mod) {
      value_delta -= value_mod;
    }

    while (index < max_index) {
      tree[index] += value_delta;
      while (tree[index] < 0) {
        tree[index] += value_mod;
      }
      while (tree[index] >= value_mod) {
        tree[index] -= value_mod;
      }
      index += (index & -index);
    }
  }

  void update(int64_t const& index, int64_t const& value) {
    update_add(index, value-tree[index]);
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

uint32_t find_incdseq(uint32_t const sequence[], int32_t const& N, int32_t const& K, int64_t const& incdseq_max_val, int64_t const& incdseq_count_mod);

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
  int64_t const incdseq_count_mod = 5000000;
  int64_t const incdseq_max_val = 100000;
  uint32_t const& total_incdseq_count = find_incdseq(sequence, N, K, incdseq_max_val, incdseq_count_mod);

  printf("%u", total_incdseq_count);

  return 0;
}

uint32_t find_incdseq(uint32_t const sequence[], int32_t const& N, int32_t const& K, int64_t const& incdseq_max_val, int64_t const& incdseq_count_mod) {
  vector<BinaryIndexedTree> BIT(K+1, BinaryIndexedTree(incdseq_max_val+1, incdseq_count_mod));

  for (int32_t N_iter=0; N_iter<N; N_iter++) {
    BIT[1].update(sequence[N_iter], 1);
    for (int32_t K_iter=2; K_iter<=K; K_iter++) {
      BIT[K_iter].update(sequence[N_iter], BIT[K_iter-1].query(sequence[N_iter]-1));
    }
  }

  return BIT[K].query(incdseq_max_val);
}
