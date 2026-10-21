# E-Textbook: Mathematical Analysis of Algorithms

An e-textbook for bachelor's students on the analysis of nonrecursive (Lecture 4)
and recursive (Lecture 5) algorithms, based on Levitin, Sections 2.3–2.5.

## Structure

| File | Content |
|------|---------|
| `index.html` | Home page, table of contents, how to use the textbook |
| `intro.html` | Review: input size, basic operation, order of growth, O/Ω/Θ, cases, entry quiz (5 questions) |
| `module1.html` | Module 1 — nonrecursive algorithms: plan, sums, worked examples, average case, mistakes, empirical check, summary and cheat sheet |
| `module1-tasks.html` | Module 1 quiz (10 questions) and 13 problems |
| `module2.html` | Module 2 — recursive algorithms: plan, backward substitution, worked examples, Fibonacci, recursion vs. iteration, summary and cheat sheet |
| `module2-tasks.html` | Module 2 quiz (10 questions) and 13 problems |
| `glossary.html`, `sources.html` | Glossary and list of sources |
| `assets/` | Styles, navigation, quiz engine, figures (`site.js`) |
| `code/` | Python code for the empirical tasks |
| `report/` | Report draft and task tracker |

Totals: 25 quiz questions (5 entry + 10 + 10) and 26 problems
(per module: 4 level A, 4 level B, 2 level C, 2 "find the mistake", 1 empirical).

## Opening the textbook locally

Double-click `index.html`. An internet connection is needed for the formulas
(MathJax is loaded from a CDN).

## Running the code

Requires Python 3.8+. `matplotlib` is optional (only for the plots).

```bash
cd code
python verify_answers.py      # checks every closed-form answer in the textbook (60 checks)
python empirical_module1.py   # task E1 of Module 1 (prints tables, saves module1_plots.png)
python empirical_module2.py   # task E1 of Module 2 (prints tables, saves module2_plots.png)
```

Install the optional dependency with `pip install matplotlib`.

## Publishing (link without installing software)

GitHub Pages, free:

1. Create a public repository on GitHub and push this folder:
   ```bash
   git remote add origin https://github.com/<user>/algo-analysis-textbook.git
   git push -u origin main
   ```
2. On GitHub: **Settings → Pages → Source: Deploy from a branch → `main` / root → Save**.
3. After a minute the textbook is available at
   `https://<user>.github.io/algo-analysis-textbook/`.

Alternative: drag-and-drop the folder to [Netlify Drop](https://app.netlify.com/drop).
