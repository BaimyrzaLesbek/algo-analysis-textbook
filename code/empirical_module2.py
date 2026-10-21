"""
Module 2 - empirical verification (task E1).

1. Fast exponentiation Power(a, n): multiplications vs log2 n + 2 (n = 2^k)
   and the bounds floor(log2 n) + 2 <= M(n) <= 2 floor(log2 n) + 2.
2. Tower of Hanoi: moves vs 2^n - 1.
3. Naive recursive Fibonacci: additions vs F(n+1) - 1, and running time.

Run:  python empirical_module2.py
Optional: pip install matplotlib   (then plots are saved to module2_plots.png)
"""

import time


def power(a, n):
    """Returns (a**n, number of multiplications)."""
    if n == 0:
        return 1, 0
    t, m = power(a, n // 2)
    if n % 2 == 0:
        return t * t, m + 1
    return t * t * a, m + 2


def hanoi(n, src="1", dst="3", aux="2"):
    """Returns the number of moves."""
    if n == 1:
        return 1
    return hanoi(n - 1, src, aux, dst) + 1 + hanoi(n - 1, aux, dst, src)


def fib_naive(n):
    """Returns (F(n), number of additions)."""
    if n <= 1:
        return n, 0
    f1, a1 = fib_naive(n - 1)
    f2, a2 = fib_naive(n - 2)
    return f1 + f2, a1 + a2 + 1


def fib_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main():
    print("Power(a, n), n = 2^k: M(n) = log2 n + 2")
    print(f"{'n':>9} {'counted':>8} {'formula':>8}")
    for k in range(21):
        n = 2 ** k
        value, m = power(2, n)
        assert value == 2 ** n
        print(f"{n:>9} {m:>8} {k + 2:>8}")

    tight = []
    for n in range(1, 10001):
        value, m = power(2, n)
        assert value == 2 ** n
        lg = n.bit_length() - 1
        assert lg + 2 <= m <= 2 * lg + 2, n
        if m == 2 * lg + 2:
            tight.append(n)
    print("\nBounds hold for all n in 1..10000.")
    print("Upper bound 2*floor(log2 n)+2 reached exactly at n =", tight)

    print("\nTower of Hanoi: M(n) = 2^n - 1")
    for n in range(1, 16):
        assert hanoi(n) == 2 ** n - 1
    print("confirmed for n = 1..15, e.g. M(10) =", hanoi(10))

    print("\nNaive Fibonacci: A(n) = F(n+1) - 1")
    for n in range(26):
        assert fib_naive(n)[1] == fib_iter(n + 1) - 1
    print("confirmed for n = 0..25")
    print(f"{'n':>4} {'additions':>12} {'time, s':>9}")
    times = []
    for n in (20, 25, 30):
        t0 = time.perf_counter()
        _, adds = fib_naive(n)
        dt = time.perf_counter() - t0
        times.append(dt)
        print(f"{n:>4} {adds:>12} {dt:>9.3f}")
    print(f"time ratio per +5: {times[1] / times[0]:.1f}, {times[2] / times[1]:.1f} "
          f"(theory: phi^5 = {((1 + 5 ** 0.5) / 2) ** 5:.1f})")

    print("\nConclusion: all formulas are confirmed; Power is Theta(log n),")
    print("Hanoi and naive Fibonacci are exponential.")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(matplotlib not installed - skipping plots)")
        return

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    ns = list(range(1, 1025))
    ms = [power(2, n)[1] for n in ns]
    lgs = [n.bit_length() - 1 for n in ns]
    axes[0].plot(ns, ms, ".", markersize=3, label="M(n) counted")
    axes[0].plot(ns, [l + 2 for l in lgs], "-", label="floor(log2 n) + 2")
    axes[0].plot(ns, [2 * l + 2 for l in lgs], "-", label="2 floor(log2 n) + 2")
    axes[0].set_title("Power(a, n): multiplications")
    axes[0].set_xlabel("n")
    axes[0].legend()

    ns = list(range(0, 26))
    axes[1].semilogy(ns, [max(fib_naive(n)[1], 1) for n in ns], "o", label="naive: additions")
    axes[1].semilogy(ns, [max(n - 1, 1) for n in ns], "s", label="iterative: n - 1")
    axes[1].set_title("Fibonacci: additions (log scale)")
    axes[1].set_xlabel("n")
    axes[1].legend()

    fig.tight_layout()
    fig.savefig("module2_plots.png", dpi=120)
    print("\nPlots saved to module2_plots.png")


if __name__ == "__main__":
    main()
