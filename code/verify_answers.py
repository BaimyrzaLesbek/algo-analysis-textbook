"""
Verifies every closed-form answer used in the e-textbook by counting
basic operations in a direct implementation and comparing with the formula.

Run:  python verify_answers.py
Every line should end with "OK". The script exits with code 1 on any mismatch.
"""

import math
import random
import sys
from fractions import Fraction
from functools import lru_cache

failures = 0


def check(name, counted, expected):
    global failures
    ok = counted == expected
    if not ok:
        failures += 1
    print(f"{'OK  ' if ok else 'FAIL'} {name}: counted={counted} expected={expected}")


def check_range(name, count_fn, formula_fn, ns):
    bad = [(n, count_fn(n), formula_fn(n)) for n in ns if count_fn(n) != formula_fn(n)]
    global failures
    if bad:
        failures += 1
        print(f"FAIL {name}: first mismatch n={bad[0][0]} counted={bad[0][1]} formula={bad[0][2]}")
    else:
        print(f"OK   {name}: n in {ns[0]}..{ns[-1]} ({len(ns)} values)")


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# ---------------------------------------------------------------------------
# Module 1 – worked examples
# ---------------------------------------------------------------------------

def max_element(n):
    a = [random.random() for _ in range(n)]
    c = 0
    maxval = a[0]
    for i in range(1, n):
        c += 1
        if a[i] > maxval:
            maxval = a[i]
    return c


def unique_elements(a):
    c = 0
    n = len(a)
    for i in range(n - 1):
        for j in range(i + 1, n):
            c += 1
            if a[i] == a[j]:
                return c
    return c


def matrix_mult(n):
    c = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c += 1
    return c


def dependent_loop(n):
    c = 0
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            c += 1
    return c


def binary_digits_iter(n):
    """Counts executions of the comparison n > 1 in Levitin's Binary(n)."""
    c = 0
    count = 1
    while True:
        c += 1
        if not n > 1:
            break
        count += 1
        n //= 2
    return c, count


def selection_sort(n):
    a = list(range(n))
    random.shuffle(a)
    c = 0
    for i in range(n - 1):
        mn = i
        for j in range(i + 1, n):
            c += 1
            if a[j] < a[mn]:
                mn = j
        a[i], a[mn] = a[mn], a[i]
    assert a == sorted(a)
    return c


def prefix_averages(n):
    a = [random.random() for _ in range(n)]
    c = 0
    for i in range(n):
        s = 0
        for j in range(i + 1):
            s += a[j]
            c += 1
    return c


def seq_search_avg_exact(n, p):
    """Exact expected comparisons, uniform position on success."""
    success = sum(Fraction(i, n) for i in range(1, n + 1))
    return p * success + (1 - p) * n


ns = list(range(1, 40))
ns2 = list(range(2, 40))
check_range("M1 MaxElement  C(n)=n-1", max_element, lambda n: n - 1, ns)
check_range("M1 UniqueElements worst C(n)=n(n-1)/2",
            lambda n: unique_elements(list(range(n))), lambda n: n * (n - 1) // 2, ns2)
check_range("M1 UniqueElements best C(n)=1",
            lambda n: unique_elements([7, 7] + list(range(n - 2))), lambda n: 1, ns2)
check_range("M1 MatrixMultiplication M(n)=n^3", matrix_mult, lambda n: n ** 3, list(range(1, 15)))
check_range("M1 Dependent loop C(n)=n(n+1)/2", dependent_loop, lambda n: n * (n + 1) // 2, ns)
check_range("M1 Binary(n) comparisons = floor(log2 n)+1",
            lambda n: binary_digits_iter(n)[0], lambda n: n.bit_length(), list(range(1, 3000)))
check_range("M1 Original SelectionSort C(n)=n(n-1)/2", selection_sort, lambda n: n * (n - 1) // 2, ns)
check_range("M1 Original PrefixAverages A(n)=n(n+1)/2", prefix_averages, lambda n: n * (n + 1) // 2, ns)
for n in (5, 10, 37):
    for p in (Fraction(0), Fraction(1, 2), Fraction(1)):
        check(f"M1 SeqSearch avg n={n} p={p}", seq_search_avg_exact(n, p),
              p * Fraction(n + 1, 2) + n * (1 - p))

# ---------------------------------------------------------------------------
# Module 1 – problems
# ---------------------------------------------------------------------------

check_range("M1-A1 count negatives C(n)=n", lambda n: sum(1 for _ in range(n)), lambda n: n, ns)
check_range("M1-A2 sum (3i+2) = (3n^2+7n)/2",
            lambda n: sum(3 * i + 2 for i in range(1, n + 1)), lambda n: (3 * n * n + 7 * n) // 2, ns)
check_range("M1-A3 terms in sum_{i=5}^{2n-1} = 2n-5",
            lambda n: len(range(5, 2 * n)), lambda n: 2 * n - 5, list(range(3, 40)))
check("M1-A4 rectangular n=7,m=4", sum(1 for i in range(7) for j in range(4)), 28)


def b1(n):
    return sum(1 for i in range(1, n + 1) for j in range(i, n + 1))


def b2(n):
    c = 0
    for i in range(n):
        for j in range(i + 1):
            for k in range(j + 1):
                c += 1
    return c


def is_sorted(a):
    c = 0
    for i in range(len(a) - 1):
        c += 1
        if a[i] > a[i + 1]:
            return c
    return c


def b4(n):
    return sum(1 for i in range(1, n + 1) for j in range(1, i * i + 1))


check_range("M1-B1 C(n)=n(n+1)/2", b1, lambda n: n * (n + 1) // 2, ns)
check_range("M1-B2 C(n)=n(n+1)(n+2)/6", b2, lambda n: n * (n + 1) * (n + 2) // 6, list(range(1, 25)))
check_range("M1-B3 IsSorted worst = n-1", lambda n: is_sorted(list(range(n))), lambda n: n - 1, ns2)
check_range("M1-B3 IsSorted best = 1", lambda n: is_sorted([1, 0] + list(range(n - 2))), lambda n: 1, ns2)
check_range("M1-B4 C(n)=n(n+1)(2n+1)/6", b4, lambda n: n * (n + 1) * (2 * n + 1) // 6, list(range(1, 25)))


def c1_exact(n, p):
    """Key at position 1 with prob 1/2, otherwise uniform on 2..n."""
    success = Fraction(1, 2) * 1 + sum(Fraction(1, 2 * (n - 1)) * i for i in range(2, n + 1))
    return p * success + (1 - p) * n


for n in (2, 3, 10, 41):
    for p in (Fraction(1, 3), Fraction(1)):
        check(f"M1-C1 skewed search n={n} p={p}", c1_exact(n, p),
              p * Fraction(n + 4, 4) + (1 - p) * n)


def c2(n):
    c = 0
    i = n
    while i >= 1:
        for _ in range(i):
            c += 1
        i //= 2
    return c


check_range("M1-C2 halving loop = 2n-1 for n=2^k", c2, lambda n: 2 * n - 1, [2 ** k for k in range(0, 16)])
check("M1-C2 halving loop <= 2n for all n<=5000", all(c2(n) <= 2 * n for n in range(1, 5001)), True)


def f2_inner(n):
    return sum(1 for i in range(n - 1) for j in range(i + 1, n))


check_range("M1-F2 correct count n(n-1)/2", f2_inner, lambda n: n * (n - 1) // 2, ns2)
check("M1-F2 student's sum equals (n-1)(n+2)/2 (n=10)", sum(10 - i for i in range(9)), 9 * 12 // 2)


def f_extra_mult_loop(n):
    c = 0
    for i in range(n):
        j = 1
        while j < n:
            j *= 2
            c += 1
    return c


# ---------------------------------------------------------------------------
# Module 2 – worked examples
# ---------------------------------------------------------------------------

def fact_mults(n):
    if n == 0:
        return 0
    return fact_mults(n - 1) + 1


def hanoi_moves(n, src="A", aux="B", dst="C"):
    if n == 1:
        return 1
    return hanoi_moves(n - 1, src, dst, aux) + 1 + hanoi_moves(n - 1, aux, src, dst)


def bin_rec_adds(n):
    if n == 1:
        return 0
    return bin_rec_adds(n // 2) + 1


def fib_adds(n):
    if n <= 1:
        return 0
    return fib_adds(n - 1) + fib_adds(n - 2) + 1


def rec_max(n):
    if n == 1:
        return 0
    return rec_max(n - 1) + 1


def power_mults(n):
    """Power(a,n): t <- Power(a, n div 2); t*t if even else t*t*a."""
    if n == 0:
        return 0
    m = power_mults(n // 2)
    return m + (1 if n % 2 == 0 else 2)


def power_value(a, n):
    if n == 0:
        return 1
    t = power_value(a, n // 2)
    return t * t if n % 2 == 0 else t * t * a


check_range("M2 Factorial M(n)=n", fact_mults, lambda n: n, list(range(0, 50)))
check_range("M2 Hanoi M(n)=2^n-1", hanoi_moves, lambda n: 2 ** n - 1, list(range(1, 16)))
check_range("M2 BinRec A(n)=floor(log2 n)", bin_rec_adds, lambda n: n.bit_length() - 1, list(range(1, 3000)))
check_range("M2 BinRec A(2^k)=k", bin_rec_adds, lambda n: int(math.log2(n)), [2 ** k for k in range(20)])
check_range("M2 Fibonacci A(n)=F(n+1)-1", fib_adds, lambda n: fib(n + 1) - 1, list(range(0, 22)))
check_range("M2 Original RecMax C(n)=n-1", rec_max, lambda n: n - 1, list(range(1, 50)))
check_range("M2 Original Power M(2^k)=log2 n + 2", power_mults,
            lambda n: n.bit_length() - 1 + 2, [2 ** k for k in range(0, 20)])
check("M2 Power computes a^n", all(power_value(3, n) == 3 ** n for n in range(60)), True)

# ---------------------------------------------------------------------------
# Module 2 – problems
# ---------------------------------------------------------------------------


def solve(rec, base_n, base_val, n):
    x = base_val
    for m in range(base_n + 1, n + 1):
        x = rec(x, m)
    return x


check_range("M2-A1 x(n)=x(n-1)+5,x(1)=0 -> 5(n-1)",
            lambda n: solve(lambda x, m: x + 5, 1, 0, n), lambda n: 5 * (n - 1), ns)
check_range("M2-A2 x(n)=3x(n-1),x(1)=4 -> 4*3^(n-1)",
            lambda n: solve(lambda x, m: 3 * x, 1, 4, n), lambda n: 4 * 3 ** (n - 1), ns)


def rec_sum_adds(n):
    if n == 1:
        return 0
    return rec_sum_adds(n - 1) + 1


check_range("M2-A3 recursive Sum A(n)=n-1", rec_sum_adds, lambda n: n - 1, ns)


def a4(n):
    return 1 if n == 1 else a4(n // 2) + 1


check_range("M2-A4 x(n)=x(n/2)+1,x(1)=1 -> log2 n + 1", a4,
            lambda n: n.bit_length(), [2 ** k for k in range(20)])
check_range("M2-B1 x(n)=x(n-1)+n,x(0)=0 -> n(n+1)/2",
            lambda n: solve(lambda x, m: x + m, 0, 0, n), lambda n: n * (n + 1) // 2, ns)


def b2_rec(n):
    return 0 if n == 1 else 2 * b2_rec(n // 2) + n


check_range("M2-B2 x(n)=2x(n/2)+n,x(1)=0 -> n log2 n", b2_rec,
            lambda n: n * (n.bit_length() - 1), [2 ** k for k in range(20)])


def tri_calls(n):
    if n == 0:
        return 0
    return 3 * tri_calls(n - 1) + 1


check_range("M2-B3 A(n)=3A(n-1)+1,A(0)=0 -> (3^n-1)/2", tri_calls,
            lambda n: (3 ** n - 1) // 2, list(range(0, 20)))
check_range("M2-B4 x(n)=x(n-1)+2n-1,x(1)=1 -> n^2",
            lambda n: solve(lambda x, m: x + 2 * m - 1, 1, 1, n), lambda n: n * n, ns)

check("M2-C1 M(n) <= 2 floor(log2 n) + 2 for n in 1..100000",
      all(power_mults(n) <= 2 * (n.bit_length() - 1) + 2 for n in range(1, 100001)), True)
check_range("M2-C1 bound is tight at n=2^k-1", power_mults,
            lambda n: 2 * (n.bit_length() - 1) + 2, [2 ** k - 1 for k in range(1, 20)])


def stairs_adds(n):
    if n <= 2:
        return 0
    return stairs_adds(n - 1) + stairs_adds(n - 2) + 1


def stairs_memo_adds(n):
    adds = 0
    memo = {1: 1, 2: 2}
    for m in range(3, n + 1):
        memo[m] = memo[m - 1] + memo[m - 2]
        adds += 1
    return adds


check_range("M2-C2 stairs A(n)=F(n)-1", stairs_adds, lambda n: fib(n) - 1, list(range(1, 25)))
check_range("M2-C2 stairs iterative = n-2 (n>=2)", stairs_memo_adds, lambda n: n - 2, list(range(2, 50)))


def halves_max(n):
    """MaxHalves(A[l..r]): split in halves, 1 comparison to combine."""
    if n == 1:
        return 0
    return halves_max(n // 2) + halves_max(n - n // 2) + 1


check_range("M2-F2 divide-and-conquer max C(n)=n-1", halves_max, lambda n: n - 1, list(range(1, 200)))

print()
if failures:
    print(f"{failures} check(s) FAILED")
    sys.exit(1)
print("All checks passed.")
