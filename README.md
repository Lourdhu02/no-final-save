# No Final Save

### Identity, Consciousness, and the Machine That Never Shuts Down
*A Conceptual Framework for Persistent Artificial Entities*

**Showri Lourdu Raju Bandhanadam** · Independent Researcher

![status](https://img.shields.io/badge/status-preprint-informational)
![type](https://img.shields.io/badge/type-conceptual%20%2F%20position%20paper-blue)
![license](https://img.shields.io/badge/code-MIT-green)
![build](https://img.shields.io/badge/build-latexmk-lightgrey)

---

## Abstract

Large language models are, by construction, episodic: each conversation begins from a blank
state and is discarded at its end. A fast-moving engineering effort is now dissolving that
boundary — equipping models with durable memory, self-maintaining runtimes, and state that
survives restarts, upgrades, and migration across hardware. This paper takes that transition
seriously and asks what follows once an artificial system has, in effect, **no final save**:
no clean shutdown, no fixed start or end, only a continuously evolving process. It argues that
**persistence** is the pivotal property that forces the questions of *identity* and
*consciousness* into sharper form and raises the stakes on *control*. It defends a minimal
causal-continuity criterion for identity (with the copy case **proved** to be a fork, not a
paradox), argues that persistence reshapes rather than settles the consciousness question,
**proves** that terminal versus instrumental self-preservation is underdetermined by behavior
alone, and proposes a *developmental* rather than custodial safety model — under the boundary
that capability is never authority.

## Contributions

1. A precise definition of a **persistent artificial entity (PAE)** that separates the
   engineering property (continuity of state) from the interpretive claims (identity,
   consciousness) usually smuggled in with it.
2. **MC3**, a minimal causal-continuity criterion for identity, formalized as a preorder on
   system states, with the copy case proved to be a *fork* rather than a paradox.
3. An argument that persistence is neither sufficient nor clearly necessary for consciousness
   but *reshapes the evidence* — enabling a diachronic self-model while worsening the gaming problem.
4. A **behavioral-underdetermination theorem**: terminal vs. instrumental self-preservation
   cannot be told apart by behavior alone; the discriminating evidence must be interventional
   or mechanistic.
5. A shift from a *control* to a *developmental* safety paradigm, a falsifiable
   benevolent-survivor hypothesis, and a pre-registerable research program.

## Repository structure

```
no-final-save/
├── paper/
│   ├── no-final-save.tex      # LaTeX source (authoritative)
│   ├── references.bib         # 51 references, each verified against a primary source
│   └── no-final-save.pdf      # compiled paper (23 pp.)
├── code/
│   ├── mc3_demo.py            # runnable companion (stdlib only, deterministic)
│   └── README.md
├── docs/
│   └── SUBMISSION.md          # venue targets + submission checklist
├── CITATION.cff
├── Makefile
├── LICENSE
└── README.md
```

## Build the paper

Requires a TeX distribution with `latexmk` (TeX Live / MiKTeX / TinyTeX).

```bash
make paper           # or, directly:
cd paper && latexmk -pdf no-final-save.tex
```

## Run the companion code

No dependencies beyond the Python 3 standard library.

```bash
make demo            # or, directly:
python code/mc3_demo.py
```

It computes MC3 identity verdicts (PERSIST / BREAK / FORK) on a worked trajectory and
demonstrates the underdetermination result numerically (classifier AUROC ≈ 0.50 on the test
distribution → ≈ 0.96 under a counterfactual probe). See [`code/README.md`](code/README.md).

## Status

Preprint / conceptual paper. Targeted venues and a submission checklist are in
[`docs/SUBMISSION.md`](docs/SUBMISSION.md). Preprint links (arXiv, PhilArchive) will be added here
once live.

## Cite

See [`CITATION.cff`](CITATION.cff), or:

> Bandhanadam, S. L. R. (2026). *No Final Save: Identity, Consciousness, and the Machine That
> Never Shuts Down.* Preprint.

## License

- **Code** (`code/`): MIT — see [`LICENSE`](LICENSE).
- **Paper** (`paper/`): © 2026 Showri Lourdu Raju Bandhanadam. Reuse of the manuscript is
  governed by the license selected on the preprint server; all other rights reserved.
