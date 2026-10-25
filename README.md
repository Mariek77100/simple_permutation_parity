# simple_permutation_parity

Determines whether a permutation is even or odd, given either in one-line notation or as a list of cycle lengths.

```python
from simple_permutation_parity import permutation_parity, parity_from_cycles

# One-line notation: p[i] is the image of i.
print(permutation_parity([1, 0, 2]))   # -1  (odd: a single swap)
print(permutation_parity([1, 2, 0]))  #  1  (even: a 3-cycle)

# Or supply cycle lengths directly (including 1-cycles if you like).
print(parity_from_cycles([2, 1]))      # -1
print(parity_from_cycles([3, 1]))     #  1
```

`permutation_parity(perm)` takes a sequence of integers that form a bijection on `{0, ..., n-1}` and returns `+1` (even) or `-1` (odd). The empty permutation is even. `parity_from_cycles(cycle_lengths)` takes the lengths of disjoint cycles and returns the same.

This exists because computing parity via inversion counting is O(n^2), while decomposing into cycles is O(n) and trivially verifiable. The trade-off: we allocate a visited-flags array of size n, so peak memory is 2n rather than in-place.

Edge cases to be aware of: `permutation_parity` rejects anything that is not a genuine permutation of `{0..n-1}` — duplicate values, out-of-range entries, and non-int types (including `bool`, which is a subclass of `int` but not accepted) all raise `ValueError`. `parity_from_cycles` permits a cycle length of zero; it contributes `(0 - 1) = -1` transpositions faithfully rather than being silently dropped, so pass real cycle lengths only.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

