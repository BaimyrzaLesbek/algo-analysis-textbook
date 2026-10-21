/* Navigation, quizzes and figures for the e-textbook. */

const NAV = [
  { group: "Start", items: [
    { href: "index.html", title: "Home & contents" },
    { href: "intro.html", title: "Introduction: review" },
  ]},
  { group: "Module 1 · Nonrecursive", items: [
    { href: "module1.html", title: "Theory & worked examples" },
    { href: "module1-tasks.html", title: "Quiz & problems" },
  ]},
  { group: "Module 2 · Recursive", items: [
    { href: "module2.html", title: "Theory & worked examples" },
    { href: "module2-tasks.html", title: "Quiz & problems" },
  ]},
  { group: "Reference", items: [
    { href: "glossary.html", title: "Glossary" },
    { href: "sources.html", title: "Sources" },
  ]},
];

function currentPage() {
  const p = location.pathname.split("/").pop();
  return p === "" ? "index.html" : p;
}

function buildSidebar() {
  const here = currentPage();
  const aside = document.createElement("nav");
  aside.className = "sidebar";
  aside.setAttribute("aria-label", "Table of contents");
  let html = `<a class="brand" href="index.html">Analysis of Algorithms<small>E-textbook for bachelor's students</small></a>`;
  for (const g of NAV) {
    html += `<h4>${g.group}</h4><ul>`;
    for (const it of g.items) {
      const active = it.href === here;
      html += `<li><a href="${it.href}"${active ? ' class="active"' : ""}>${it.title}</a></li>`;
      if (active) {
        document.querySelectorAll("main h2[id]").forEach(h => {
          html += `<li class="sub"><a href="#${h.id}">${h.dataset.short || h.textContent}</a></li>`;
        });
      }
    }
    html += `</ul>`;
  }
  aside.innerHTML = html;

  const btn = document.createElement("button");
  btn.className = "menu-toggle";
  btn.textContent = "\u2630 Contents";
  btn.onclick = () => aside.classList.toggle("open");

  const layout = document.querySelector(".layout");
  layout.prepend(aside);
  layout.prepend(btn);
}

function buildPageNav() {
  const flat = NAV.flatMap(g => g.items);
  const i = flat.findIndex(it => it.href === currentPage());
  const nav = document.querySelector(".page-nav");
  if (!nav || i < 0) return;
  const prev = flat[i - 1], next = flat[i + 1];
  nav.innerHTML =
    (prev ? `<a href="${prev.href}">\u2190 ${prev.title}</a>` : "<span></span>") +
    (next ? `<a href="${next.href}">${next.title} \u2192</a>` : "<span></span>");
}

/* ------------------------------------------------------------------ quiz */

function renderQuiz(containerId, questions) {
  const root = document.getElementById(containerId);
  if (!root) return;
  root.classList.add("quiz");
  let answered = 0, correct = 0;

  const score = document.createElement("div");
  score.className = "score";

  const update = () => {
    score.innerHTML = answered < questions.length
      ? `Answered ${answered} of ${questions.length}. Correct so far: ${correct}.`
      : `Done! Score: ${correct} / ${questions.length}. ` +
        (correct === questions.length ? "Excellent." :
         correct >= questions.length * 0.7 ? "Good — reread the explanations for the ones you missed." :
         "Review the theory section and try again.");
  };

  questions.forEach((q, qi) => {
    const box = document.createElement("div");
    box.className = "q";
    box.innerHTML = `<div class="q-text">${qi + 1}. ${q.q}</div>`;
    q.options.forEach((o) => {
      const b = document.createElement("button");
      b.className = "opt";
      b.innerHTML = o.t;
      const why = document.createElement("div");
      why.className = "why" + (o.ok ? " correct" : "");
      why.innerHTML = (o.ok ? "\u2714 Correct: " : "\u2718 Incorrect: ") + o.why;
      b.onclick = () => {
        if (box.classList.contains("answered")) return;
        box.classList.add("answered");
        answered++;
        if (o.ok) correct++;
        else { b.classList.add("wrong"); why.classList.add("chosen-wrong"); }
        box.querySelectorAll(".opt").forEach(x => x.disabled = true);
        box.querySelectorAll(".opt").forEach((x, k) => { if (q.options[k].ok) x.classList.add("correct"); });
        update();
      };
      box.appendChild(b);
      box.appendChild(why);
    });
    root.appendChild(box);
  });

  const reset = document.createElement("button");
  reset.className = "reset";
  reset.textContent = "Reset quiz";
  reset.onclick = () => { root.innerHTML = ""; renderQuiz(containerId, questions); };
  update();
  root.appendChild(score);
  root.appendChild(reset);
  if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([root]);
}

/* --------------------------------------------------------------- figures */

const SVG_NS = "http://www.w3.org/2000/svg";

function svgEl(tag, attrs, text) {
  const e = document.createElementNS(SVG_NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (text !== undefined) e.textContent = text;
  return e;
}

/* Growth-of-functions chart. */
function drawGrowthChart(id, opts = {}) {
  const host = document.getElementById(id);
  if (!host) return;
  const W = 680, H = 400, L = 56, R = 150, T = 20, B = 44;
  const nMax = opts.nMax || 20, yMax = opts.yMax || 400;
  const fns = [
    { name: "log\u2082 n", f: n => Math.log2(n), c: "#1d7a46" },
    { name: "n", f: n => n, c: "#2f5fd0" },
    { name: "n log\u2082 n", f: n => n * Math.log2(n), c: "#7a4a00" },
    { name: "n\u00B2", f: n => n * n, c: "#b3261e" },
    { name: "n\u00B3", f: n => n ** 3, c: "#5b3fc4" },
    { name: "2\u207F", f: n => 2 ** n, c: "#000" },
  ];
  const svg = svgEl("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img" });
  const x = n => L + (n / nMax) * (W - L - R);
  const y = v => H - B - (Math.min(v, yMax) / yMax) * (H - T - B);

  for (let k = 0; k <= 4; k++) {
    const v = (yMax / 4) * k;
    svg.appendChild(svgEl("line", { x1: L, x2: W - R, y1: y(v), y2: y(v), stroke: "#eee" }));
    svg.appendChild(svgEl("text", { x: L - 8, y: y(v) + 4, "text-anchor": "end", "font-size": 12, fill: "#666" }, v));
  }
  for (let n = 0; n <= nMax; n += nMax / 5) {
    svg.appendChild(svgEl("text", { x: x(n), y: H - B + 18, "text-anchor": "middle", "font-size": 12, fill: "#666" }, n));
  }
  svg.appendChild(svgEl("line", { x1: L, x2: W - R, y1: H - B, y2: H - B, stroke: "#333" }));
  svg.appendChild(svgEl("line", { x1: L, x2: L, y1: T, y2: H - B, stroke: "#333" }));
  svg.appendChild(svgEl("text", { x: (L + W - R) / 2, y: H - 6, "text-anchor": "middle", "font-size": 13 }, "input size n"));
  svg.appendChild(svgEl("text", { x: 14, y: (T + H - B) / 2, "font-size": 13, transform: `rotate(-90 14 ${(T + H - B) / 2})`, "text-anchor": "middle" }, "number of basic operations"));

  fns.forEach((fn, i) => {
    let d = "";
    for (let n = 1; n <= nMax; n += 0.1) {
      const v = fn.f(n);
      d += (d ? "L" : "M") + x(n).toFixed(1) + "," + y(v).toFixed(1);
      if (v > yMax) break;
    }
    svg.appendChild(svgEl("path", { d, fill: "none", stroke: fn.c, "stroke-width": 2.5 }));
    svg.appendChild(svgEl("rect", { x: W - R + 18, y: T + 10 + i * 24, width: 16, height: 4, fill: fn.c }));
    svg.appendChild(svgEl("text", { x: W - R + 40, y: T + 16 + i * 24, "font-size": 14 }, fn.name));
  });
  host.appendChild(svg);
}

/* Grid showing which (i, j) pairs a nested loop visits. */
function drawLoopGrid(id, n, visit) {
  const host = document.getElementById(id);
  if (!host) return;
  const cell = 34, pad = 40;
  const W = pad + n * cell + 20, H = pad + n * cell + 20;
  const svg = svgEl("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H });
  for (let i = 1; i <= n; i++) {
    svg.appendChild(svgEl("text", { x: pad - 10, y: pad + (i - 0.5) * cell + 5, "text-anchor": "end", "font-size": 13 }, "i=" + i));
    for (let j = 1; j <= n; j++) {
      const on = visit(i, j);
      svg.appendChild(svgEl("rect", {
        x: pad + (j - 1) * cell + 2, y: pad + (i - 1) * cell + 2, width: cell - 4, height: cell - 4, rx: 5,
        fill: on ? "#2f5fd0" : "#f1f1ee", stroke: on ? "#24489e" : "#ddd",
      }));
    }
  }
  for (let j = 1; j <= n; j++) {
    svg.appendChild(svgEl("text", { x: pad + (j - 0.5) * cell, y: pad - 10, "text-anchor": "middle", "font-size": 13 }, "j=" + j));
  }
  host.appendChild(svg);
}

/* Binary recursion tree. children(label) returns [] or child labels. */
function drawTree(id, rootLabel, children, opts = {}) {
  const host = document.getElementById(id);
  if (!host) return;
  const levelH = opts.levelH || 70, nodeW = opts.nodeW || 46;
  const leaves = [];
  function build(label, depth) {
    const node = { label, depth, kids: children(label).map(c => build(c, depth + 1)) };
    if (!node.kids.length) leaves.push(node);
    return node;
  }
  const root = build(rootLabel, 0);
  let maxDepth = 0;
  leaves.forEach((lf, i) => { lf.x = i; });
  (function place(nd) {
    maxDepth = Math.max(maxDepth, nd.depth);
    if (nd.kids.length) {
      nd.kids.forEach(place);
      nd.x = (nd.kids[0].x + nd.kids[nd.kids.length - 1].x) / 2;
    }
  })(root);
  const W = Math.max(leaves.length * nodeW + 40, 300) + (opts.rightPad || 0);
  const H = (maxDepth + 1) * levelH + 20;
  const svg = svgEl("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H });
  const px = nd => 20 + nd.x * nodeW + nodeW / 2;
  const py = nd => 30 + nd.depth * levelH;
  (function edges(nd) {
    nd.kids.forEach(k => {
      svg.appendChild(svgEl("line", { x1: px(nd), y1: py(nd), x2: px(k), y2: py(k), stroke: "#999" }));
      edges(k);
    });
  })(root);
  (function nodes(nd) {
    const fill = opts.color ? opts.color(nd.label) : "#e8eefc";
    svg.appendChild(svgEl("circle", { cx: px(nd), cy: py(nd), r: 17, fill, stroke: "#24489e" }));
    svg.appendChild(svgEl("text", { x: px(nd), y: py(nd) + 5, "text-anchor": "middle", "font-size": 13, "font-weight": 600 }, opts.fmt ? opts.fmt(nd.label) : nd.label));
    nd.kids.forEach(nodes);
  })(root);
  if (opts.levelText) {
    for (let d = 0; d <= maxDepth; d++) {
      svg.appendChild(svgEl("text", { x: W - 10, y: 30 + d * levelH + 5, "text-anchor": "end", "font-size": 13, fill: "#7a4a00" }, opts.levelText(d)));
    }
  }
  host.appendChild(svg);
}

/* Call stack of a linear recursion (e.g. factorial). */
function drawStack(id, n) {
  const host = document.getElementById(id);
  if (!host) return;
  const h = 34, W = 420, H = (n + 1) * h + 60;
  const svg = svgEl("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H });
  for (let k = 0; k <= n; k++) {
    const yy = H - 30 - (k + 1) * h;
    svg.appendChild(svgEl("rect", { x: 60, y: yy, width: 220, height: h - 4, rx: 6, fill: k === n ? "#ffe8c7" : "#e8eefc", stroke: "#24489e" }));
    const text = k === n ? "F(0) = 1  (base case)" : `F(${n - k})  waits for F(${n - k - 1})`;
    svg.appendChild(svgEl("text", { x: 170, y: yy + h / 2 + 3, "text-anchor": "middle", "font-size": 14 }, text));
  }
  svg.appendChild(svgEl("text", { x: 170, y: H - 8, "text-anchor": "middle", "font-size": 13, fill: "#666" }, "bottom of the stack: first call"));
  svg.appendChild(svgEl("line", { x1: 310, y1: H - 34, x2: 310, y2: H - 30 - (n + 1) * h, stroke: "#b3261e", "stroke-width": 2, "marker-end": "url(#arr)" }));
  const defs = svgEl("defs", {});
  const m = svgEl("marker", { id: "arr", markerWidth: 10, markerHeight: 10, refX: 5, refY: 5, orient: "auto" });
  m.appendChild(svgEl("path", { d: "M0,0 L10,5 L0,10 z", fill: "#b3261e" }));
  defs.appendChild(m);
  svg.prepend(defs);
  svg.appendChild(svgEl("text", { x: 320, y: H / 2, "font-size": 13, fill: "#b3261e" }, `depth = ${n + 1}`));
  svg.appendChild(svgEl("text", { x: 320, y: H / 2 + 18, "font-size": 13, fill: "#b3261e" }, "frames"));
  host.appendChild(svg);
}

/* Interactive operation counter: compares a counted value with a formula. */
function opCounterWidget(id, algos) {
  const host = document.getElementById(id);
  if (!host) return;
  host.classList.add("widget");
  host.innerHTML = `
    <label>Algorithm: <select class="alg">${algos.map((a, i) => `<option value="${i}">${a.name}</option>`).join("")}</select></label>
    <br><label>n = <span class="nval"></span> <input type="range" class="n" min="1" max="30" value="8"></label>
    <div class="out"></div>`;
  const sel = host.querySelector(".alg"), rng = host.querySelector(".n");
  const out = host.querySelector(".out"), nv = host.querySelector(".nval");
  const run = () => {
    const a = algos[+sel.value];
    rng.min = a.min || 1; rng.max = a.max || 30;
    const n = +rng.value;
    nv.textContent = n;
    const c = a.count(n), f = a.formula(n);
    out.innerHTML = `counted by running the loops: <b>${c}</b><br>formula ${a.formulaText}: <b>${f}</b> ` +
      (c === f ? `<span style="color:var(--ok)">\u2714 match</span>` : `<span style="color:var(--bad)">\u2718 mismatch</span>`);
  };
  sel.onchange = run; rng.oninput = run; run();
}

document.addEventListener("DOMContentLoaded", () => {
  buildSidebar();
  buildPageNav();
});
