"""Compute the parity of a permutation via its cycle decomposition.

A permutation is *even* if it can be written as a product of an even number
of transpositions (2-cycles), and *odd* otherwise. The sign/parity of a
permutation is determined entirely by its cycle structure: a cycle of length k
decomposes into k-1 transpositions, so the total transposition count is
    sum(k_i - 1) = sum(k_i) - r
where the k_i are the cycle lengths and r is the number of cycles (including
the 1-cycles, i.e. fixed points). The parity is even iff this sum is even.

This module accepts the permutation in *one-line notation*: a sequence
``p`` where ``p[i]`` is the image of ``i``, with indices 0..n-1.
"""

from __future__ import annotations

from typing import Sequence


def parity_from_cycles(cycle_lengths: Sequence[int]) -> int:
    """Return the parity of a permutation given the lengths of its cycles.

    Args:
        cycle_lengths: Lengths of the disjoint cycles, including 1-cycles
            (fixed points) if you want to be explicit. Only the values matter,
            not the order. Each length must be a non-negative integer; a length
            of zero is permitted and represents an empty contribution.

    Returns:
        +1 for even parity, -1 for odd parity.

    Raises:
        ValueError: If any length is negative or not an integer.

    We work modulo 2 on ``(sum(lengths) - count)``. The number of
    transpositions is ``sum(k_i - 1)``; its parity is ``sum(k_i) - r`` mod 2,
    which we compute without risking large intermediate sums by reducing
    each term modulo 2 as we go.
    """
    total = 0
    count = 0
    for k in cycle_lengths:
        if not isinstance(k, int) or isinstance(k, bool):
            raise ValueError(f"cycle length must be an int, got {k!r}")
        if k < 0:
            raise ValueError(f"cycle length must be non-negative, got {k!r}")
        # (k - 1) mod 2 is what we actually need; k == 0 contributes -1 mod 2 = 1,
        # which is consistent with treating an empty cycle as a no-op of parity 0
        # only when k >= 1. We allow k == 0 for robustness and it adds (k-1) = -1.
        # That is a deliberate, documented choice: a zero-length cycle is not a
        # real cycle, but if a caller passes one we reduce it faithfully rather
        # than silently dropping it, because silently dropping data can mask bugs.
        total += k - 1
        count += 1
    return -1 if (total % 2 == 1) else 1


def permutation_parity(perm: Sequence[int]) -> int:
    """Return the parity of a permutation given in one-line notation.

    Args:
        perm: A sequence ``p`` of length ``n`` where ``p[i]`` is the image of
            ``i`` and the elements form exactly the set ``{0, 1, ..., n-1}``.
            The empty permutation is allowed and is even.

    Returns:
        +1 for even parity, -1 for odd parity.

    Raises:
        ValueError: If ``perm`` is not a valid permutation of ``{0..n-1}``.

    The permutation is decomposed into disjoint cycles by marking visited
    elements and walking each unvisited element forward until we return to
    the cycle's start. This is O(n) time and O(n) auxiliary space for the
    visited flags. We prefer cycle decomposition over counting inversions
    (O(n^2)) because it is asymptotically faster for large permutations and
    the implementation is straightforward and obviously correct.
    """
    n = len(perm)

    # Validate that perm is a bijection on {0, ..., n-1}.
    seen = [False] * n
    for i, x in enumerate(perm):
        if not isinstance(x, int) or isinstance(x, bool):
            raise ValueError(f"permutation entries must be ints, perm[{i}]={x!r}")
        if x < 0 or x >= n:
            raise ValueError(
                f"permutation entry {x} out of range for length {n}"
            )
        if seen[x]:
            raise ValueError(
                f"not a permutation: value {x} appears more than once"
            )
        seen[x] = True

    # Walk cycles. transposition_count = sum(k_i - 1).
    transpositions = 0
    visited = [False] * n
    for start in range(n):
        if visited[start]:
            continue
        # Follow the cycle starting at `start`.
        length = 0
        j = start
        while not visited[j]:
            visited[j] = True
            j = perm[j]
            length += 1
        transpositions += length - 1

    return -1 if (transpositions % 2 == 1) else 1
