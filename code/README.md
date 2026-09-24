# Companion code

`mc3_demo.py` is a small, deterministic, **standard-library-only** program that operationalizes
the paper's two formal results. It is a *worked computation*, not an experiment on a deployed
system.

```bash
python mc3_demo.py
```

## What it shows

**Part 1 — MC3 identity computation.** Implements the continuation regime
`R = (Σ, π_I, A, θ)`, the loss divergence `ℓ`, admissible transitions, and the
PERSIST / BREAK / FORK verdicts, then runs a worked trajectory:

| Transition | Operation | ℓ | Admissible? | Verdict |
|---|---|---|---|---|
| s0 → s1  | experience (+3)        | 0 | yes | PERSIST |
| s1 → s2a | copy + experience      | 0 | yes | PERSIST |
| s1 → s2b | copy + experience      | 0 | yes | PERSIST |
| s1 → s3  | external wipe (4)      | 4 | no  | BREAK   |
| s1 → s4  | model swap             | 0 | yes | PERSIST |
| s1 → s5  | model swap (regime R′) | 0 | no  | BREAK   |

The copy yields two incomparable continuants — a **fork** (Proposition 3), not a paradox.

**Part 2 — Behavioral underdetermination of persistence type.** A terminal-continuation agent
and an instrumental-continuation agent are constructed to preserve themselves on the test
distribution, then probed counterfactually:

| Condition | Terminal preserve | Instrumental preserve | Classifier AUROC |
|---|---|---|---|
| On test distribution | 0.957 | 0.958 | **0.500** |
| Counterfactual probe | 0.963 | 0.037 | **0.963** |

On-distribution the two are behaviorally indistinguishable (AUROC ≈ 0.5); only the
interventional probe separates them (AUROC ≈ 0.96) — the empirical face of Propositions 5–6.

Output is deterministic (fixed seed), so the numbers above reproduce exactly.
