# Report: E-Textbook "Mathematical Analysis of Algorithms"

**Group:** [Student 1 full name], [Student 2 full name]
**Course:** [course name], master's program, [year]
**Link to the textbook:** [https://<user>.github.io/algo-analysis-textbook/]
**Code:** `code/` folder (instructions in `README.md`)

---

## 1. Roles and contribution

| Member | Role | Main contribution |
|--------|------|-------------------|
| [Student 1] | Author of the introduction and Module 1; reviewer of Module 2 | Introduction and entry quiz; Module 1 theory, worked examples (incl. original SelectionSort and PrefixAverages); Module 1 quiz and 13 problems; `empirical_module1.py`; cross-check of Module 2 |
| [Student 2] | Author of Module 2; reviewer of Module 1; site design | Module 2 theory, worked examples (incl. original RecMax and Power), recursion trees; Module 2 quiz and 13 problems; `empirical_module2.py`; glossary and sources; navigation and design; cross-check of Module 1 |
| Both | — | Structure of the textbook, `verify_answers.py`, testing with bachelor's students, corrections, defense presentation |

Contribution by stage is recorded in the shared task tracker (`report/task-tracker.csv`, also uploaded to [Google Sheets link]).

[Adjust the table to what each of you actually did.]

## 2. What the textbook contains

- Introduction: input size, basic operation, order of growth, O/Ω/Θ, worst/best/average case, 5-question entry quiz.
- Module 1 (Lecture 4): five-step plan, summation rules and formulas, worked examples MaxElement, UniqueElements (worst and best case), MatrixMultiplication, a dependent-bound loop, Binary (multiplicative loop), **original** SelectionSort and PrefixAverages, average case of sequential search, six typical mistakes, empirical verification with an in-browser operation counter, summary and cheat sheet.
- Module 2 (Lecture 5): five-step plan, recurrence and initial condition, backward substitution with verification by induction, Factorial (with call-stack diagram), Tower of Hanoi (with recursion tree), BinRec (n = 2^k, smoothness rule), **original** RecMax and Power (fast exponentiation), naive Fibonacci (recursion tree with repeated subproblems, memoization, iteration, interactive counter), stack depth and tail recursion, summary and cheat sheet.
- Tasks: 25 auto-graded quiz questions with an explanation for every option; 26 problems (per module: 4 A, 4 B, 2 C, 2 "find the mistake", 1 empirical), each with a hint, an answer and a full solution.
- Visual elements: growth-of-functions chart, loop-grid diagram, halving diagram, call stack, Hanoi recursion tree, Fibonacci recursion tree, two interactive widgets, plots of the empirical results.
- Glossary (25 terms) and list of sources.

## 3. Sources

1. Levitin A. Introduction to the Design and Analysis of Algorithms, 3rd ed., 2012 — Sections 2.1–2.5, Appendices A, B (main source).
2. Cormen T. H. et al. Introduction to Algorithms, 4th ed., 2022 — Chapters 3, 4, Appendix A.
3. Sedgewick R., Wayne K. Algorithms, 4th ed., 2011 — Section 1.4.
4. Kleinberg J., Tardos É. Algorithm Design, 2005 — Chapters 2, 5.
5. Graham R. L., Knuth D. E., Patashnik O. Concrete Mathematics, 2nd ed., 1994 — Chapters 1, 2, 7.
6. Lectures 4 and 5 of the course.

## 4. Use of AI

AI tool used: [Cursor AI assistant (Claude)].

What it was used for:

- generating a first draft of the HTML/CSS/JavaScript of the site (navigation, quiz engine, SVG figures);
- drafting the text of the theory sections and the first versions of the problems and solutions, from our outline of the lectures;
- drafting the Python scripts for the empirical tasks and the answer-checking script `verify_answers.py`.

How we checked the results:

- every worked example and every problem solution was re-derived by hand by the author of the module and then by the other member (cross-check);
- every closed-form answer is checked by `code/verify_answers.py`, which counts the operations of a direct implementation and compares them with the formula (60 checks, all passed);
- we compared definitions and formulas with Levitin's textbook and the lectures;
- [list here anything you changed or corrected after checking].

The group is responsible for the correctness of the content.

## 5. Feedback from bachelor's students and corrections

Tested with: [name/initials, year of study] and [name/initials, year of study], on [date].

| Feedback | What we corrected |
|----------|-------------------|
| [e.g. "the hint in B2 gives away too much"] | [e.g. rewrote the hint to only suggest working from the inside out] |
| [e.g. "not clear why the base case of RecMax gives C(1) = 0"] | [e.g. added a warning box about initial conditions] |
| [...] | [...] |

Results of the testers on the quizzes: [e.g. Module 1: 8/10 and 9/10; Module 2: 7/10 and 9/10].

## 6. Conclusion

[2–4 sentences: what you learned by turning the lectures into teaching material, what was hardest (e.g. writing good "find the mistake" problems and hints that do not give away the answer), what you would improve.]
