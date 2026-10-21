"""
Module 1 - empirical verification (task E1).

Counts basic operations in nonrecursive algorithms and compares the counts
with the formulas derived in the textbook.

Run:  python empirical_module1.py
Optional: pip install matplotlib   (then plots are saved to module1_plots.png)
"""


def unique_elements(a):
    """Example 1.2. Returns (result, number of comparisons A[i] = A[j])."""
    count = 0
    n = len(a)
    for i in range(n - 1):
        for j in range(i + 1, n):
            count += 1
            if a[i] == a[j]:
                return False, count
    return True, count


def b2(n):
    """Problem B2: three nested loops with dependent bounds."""
    count = 0
    for i in range(n):
        for j in range(i + 1):
            for k in range(j + 1):
                count += 1
    return count


def c2(n):
    """Problem C2: halving outer loop, inner loop runs i times."""
    count = 0
    i = n
    while i >= 1:
        for _ in range(i):
            count += 1
        i //= 2
    return count


def table(title, rows, g_name):
    print(f"\n{title}")
    print(f"{'n':>7} {'counted':>12} {'formula':>12} {'equal':>6} {'counted/' + g_name:>14}")
    for n, counted, formula, ratio in rows:
        print(f"{n:>7} {counted:>12} {formula:>12} {str(counted == formula):>6} {ratio:>14.4f}")


def main():
    rows = []
    for n in [10, 100, 1000]:
        _, c = unique_elements(list(range(n)))          # distinct -> worst case
        rows.append((n, c, n * (n - 1) // 2, c / n ** 2))
    table("UniqueElements, worst case: C(n) = n(n-1)/2", rows, "n^2")

    rows = []
    for n in [5, 10, 20, 40, 80]:
        c = b2(n)
        rows.append((n, c, n * (n + 1) * (n + 2) // 6, c / n ** 3))
    table("B2: C(n) = n(n+1)(n+2)/6", rows, "n^3")

    rows = []
    for k in range(4, 15, 2):
        n = 2 ** k
        c = c2(n)
        rows.append((n, c, 2 * n - 1, c / n))
    table("C2 (n = 2^k): C(n) = 2n - 1", rows, "n")

    print("\nConclusion: the counted values equal the formulas exactly.")
    print("B2: counted/n^3 -> 1/6 = 0.1667, so C(n) is Theta(n^3) with leading constant 1/6.")
    print("C2: counted/n -> 2, so C(n) is Theta(n), not Theta(n log n).")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(matplotlib not installed - skipping plots)")
        return

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    ns = list(range(1, 41))
    axes[0].plot(ns, [b2(n) for n in ns], "o", label="counted")
    axes[0].plot(ns, [n * (n + 1) * (n + 2) / 6 for n in ns], "-", label="n(n+1)(n+2)/6")
    axes[0].set_title("B2: three dependent loops")
    axes[0].set_xlabel("n")
    axes[0].legend()

    ns = list(range(1, 257))
    axes[1].plot(ns, [c2(n) for n in ns], ".", label="counted (all n)")
    axes[1].plot(ns, [2 * n - 1 for n in ns], "-", label="2n - 1")
    axes[1].plot(ns, ns, "--", label="n")
    axes[1].set_title("C2: halving outer loop")
    axes[1].set_xlabel("n")
    axes[1].legend()

    fig.tight_layout()
    fig.savefig("module1_plots.png", dpi=120)
    print("\nPlots saved to module1_plots.png")


if __name__ == "__main__":
    main()
