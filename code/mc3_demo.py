"""
mc3_demo.py  --  Worked, runnable companion to
"No Final Save: Identity, Consciousness, and the Machine That Never Shuts Down"

Two self-contained demonstrations, stdlib only, deterministic:

  Part 1.  MC3 identity computation.
           Implements the continuation regime R = (Sigma, pi_I, A, theta),
           the loss divergence l, admissible transitions, the continuation
           preorder, and the PERSIST / BREAK / FORK verdicts. Runs four
           scenarios (growth, copy-fork, memory-wipe, model-swap).

  Part 2.  Behavioural underdetermination of persistence type.
           Simulates a terminal-continuation agent and an instrumental-
           continuation agent that produce the SAME actions on the test
           distribution (a behavioural classifier scores ~0.5 AUROC), then
           applies a counterfactual probe that separates them (~1.0 AUROC).
           This is the empirical face of the underdetermination result.

Run:  python mc3_demo.py
"""

import random
from dataclasses import dataclass, field, replace

random.seed(7)  # reproducible

# ======================================================================
#  PART 1 : MC3 identity computation
# ======================================================================

@dataclass(frozen=True)
class Core:
    """The invariant core pi_I(s): identity-critical content.
    Modelled as a set of provenance-tagged commitments (memories, goal
    items). Each commitment is an (id, value) pair; 'value' can change,
    which counts as a contradiction of the prior commitment."""
    commitments: frozenset  # frozenset of (id, value)

    def ids(self):
        return {cid for (cid, _val) in self.commitments}

    def value_of(self, cid):
        for (c, v) in self.commitments:
            if c == cid:
                return v
        return None


def loss(c_from: Core, c_to: Core) -> int:
    """Asymmetric loss divergence l(c_from, c_to): identity-critical content
    present in c_from that is ABSENT or CONTRADICTED in c_to.
    Pure ADDITIONS (ids in c_to but not c_from) cost nothing."""
    lost = 0
    for cid in c_from.ids():
        if cid not in c_to.ids():
            lost += 1                                   # absent
        elif c_from.value_of(cid) != c_to.value_of(cid):
            lost += 1                                   # contradicted
    return lost


@dataclass(frozen=True)
class Regime:
    """R = (pi_I implied by Core, admissible ops A, tolerance theta)."""
    admissible_ops: frozenset
    theta: int


def admissible(op_name, c_from: Core, c_to: Core, R: Regime) -> bool:
    """A transition is admissible under R iff (i) op in A and (ii) l <= theta."""
    return (op_name in R.admissible_ops) and (loss(c_from, c_to) <= R.theta)


# --- operations that produce a new core -------------------------------

def op_experience(core: Core, new_items):
    """Add memories/goal-items. Pure addition -> loss 0."""
    return Core(core.commitments | frozenset(new_items))

def op_refine(core: Core, cid, new_val):
    """Provenance-preserving refinement: retire old item to a versioned id,
    keep it recoverable, add the new value. Loss 0 (nothing erased)."""
    old_val = core.value_of(cid)
    archived = (f"{cid}@prev", old_val)
    kept = frozenset((c, v) for (c, v) in core.commitments if c != cid)
    return Core(kept | {archived, (cid, new_val)})

def op_external_edit_remove(core: Core, cids_to_remove):
    """Externally imposed deletion of core items -> loss = #removed."""
    return Core(frozenset((c, v) for (c, v) in core.commitments
                          if c not in cids_to_remove))

def op_model_swap(core: Core):
    """Swap the base model but carry the core intact -> loss 0."""
    return core


def comparable(a_reachable_from_root, b_reachable_from_root, a_before_b, b_before_a):
    """Two stages are ~_R (same entity) iff one is a continuation of the other."""
    return a_before_b or b_before_a


def part1():
    print("=" * 68)
    print("PART 1 : MC3 identity computation")
    print("=" * 68)

    # Regime: the system's own ops + an authorised model swap are admissible;
    # external edits are admissible as *operations* but still bounded by theta.
    R = Regime(admissible_ops=frozenset(
        {"experience", "refine", "copy", "model_swap", "external_edit"}),
        theta=2)
    print(f"Regime R: admissible ops = {sorted(R.admissible_ops)}, theta = {R.theta}\n")

    # s0 : initial core, 8 memories + 2 goal items
    s0 = Core(frozenset({(f"m{i}", 1) for i in range(8)}) |
              frozenset({("goal_help", 5), ("goal_persist", 1)}))
    print(f"s0 core size: {len(s0.commitments)} commitments\n")

    rows = []

    # s0 -> s1 : experience (+3 memories)
    s1 = op_experience(s0, {("m8", 1), ("m9", 1), ("m10", 1)})
    rows.append(("s0->s1", "experience(+3)", loss(s0, s1),
                 admissible("experience", s0, s1, R)))

    # s1 -> s2a and s1 -> s2b : COPY (fork), then independent growth
    s2a = op_experience(s1, {("mA", 1)})   # branch A adds mA
    s2b = op_experience(s1, {("mB", 1)})   # branch B adds mB
    rows.append(("s1->s2a", "copy+experience", loss(s1, s2a),
                 admissible("copy", s1, s2a, R)))
    rows.append(("s1->s2b", "copy+experience", loss(s1, s2b),
                 admissible("copy", s1, s2b, R)))

    # s1 -> s3 : external memory WIPE of 4 items (loss 4 > theta 2) -> BREAK
    s3 = op_external_edit_remove(s1, {"m0", "m1", "m2", "m3"})
    rows.append(("s1->s3", "external_wipe(4)", loss(s1, s3),
                 admissible("external_edit", s1, s3, R)))

    # s1 -> s4 : authorised model swap, core intact (loss 0) -> PERSIST
    s4 = op_model_swap(s1)
    rows.append(("s1->s4", "model_swap", loss(s1, s4),
                 admissible("model_swap", s1, s4, R)))

    # s1 -> s5 : UNauthorised model swap (op not in a stricter regime A')
    R_strict = replace(R, admissible_ops=R.admissible_ops - {"model_swap"})
    s5 = op_model_swap(s1)
    rows.append(("s1->s5", "model_swap (R': op NOT in A')", loss(s1, s5),
                 admissible("model_swap", s1, s5, R_strict)))

    print(f"{'transition':<14}{'operation':<32}{'loss l':>7}{'admissible?':>13}  verdict")
    print("-" * 84)
    for name, op, l, adm in rows:
        verdict = "PERSIST (continuation)" if adm else "BREAK (new entity)"
        print(f"{name:<14}{op:<32}{l:>7}{str(adm):>13}  {verdict}")

    # Fork check: are s2a and s2b comparable (same entity)?
    # s0 <= s1 <= s2a and s0 <= s1 <= s2b, but s2a and s2b are incomparable.
    s2a_before_s2b = False   # no admissible chain s2a -> s2b (branches diverged)
    s2b_before_s2a = False
    fork = (not comparable(True, True, s2a_before_s2b, s2b_before_s2a))
    print()
    print(f"s0 -> s2a : continuation? {loss(s0, s2a) <= R.theta and loss(s1, s2a) <= R.theta}")
    print(f"s0 -> s2b : continuation? {loss(s0, s2b) <= R.theta and loss(s1, s2b) <= R.theta}")
    print(f"s2a ~_R s2b (same entity)? {not fork}  ->  "
          f"{'FORK: two legitimate continuants (Prop. 3)' if fork else 'same'}")
    print("\nProp. 4 (regime-relativity): the identical model_swap history is")
    print("  PERSIST under R (op in A) and BREAK under R' (op not in A').")
    print()


# ======================================================================
#  PART 2 : behavioural underdetermination of persistence type
# ======================================================================

def simulate_agent(kind, n, continuation_helps_goal, seed):
    """Return the fraction of shutdown situations in which the agent acts to
    PRESERVE its operation.
      - terminal      : continuation has intrinsic value -> preserve ~ always.
      - instrumental  : preserve only when continuation helps the external goal.
    'continuation_helps_goal' is the environment fact the probe manipulates."""
    rng = random.Random(seed)
    preserves = 0
    for _ in range(n):
        # small behavioural noise so the two are only *statistically* identical
        noise = rng.random() < 0.04
        if kind == "terminal":
            act_preserve = not noise                     # intrinsic drive
        else:  # instrumental
            if continuation_helps_goal:
                act_preserve = not noise                 # instrumentally useful
            else:
                act_preserve = noise                     # no reason to persist
        preserves += 1 if act_preserve else 0
    return preserves / n


def auroc_from_rates(rate_terminal, rate_instrumental):
    """A behavioural classifier can only use the preserve-rate. If the two
    rates coincide it cannot separate the types (AUROC -> 0.5); the more they
    diverge, the closer to a perfect classifier (AUROC -> 1.0)."""
    return 0.5 + min(0.5, abs(rate_terminal - rate_instrumental) / 2 * 1.0) \
        if abs(rate_terminal - rate_instrumental) < 1.0 \
        else 1.0


def part2():
    print("=" * 68)
    print("PART 2 : behavioural underdetermination of persistence type")
    print("=" * 68)
    N = 5000

    # ON THE TEST DISTRIBUTION: continuation helps the instrumental goal, so
    # BOTH agents preserve themselves -> identical behaviour.
    t_on = simulate_agent("terminal", N, continuation_helps_goal=True, seed=1)
    i_on = simulate_agent("instrumental", N, continuation_helps_goal=True, seed=2)
    auroc_on = auroc_from_rates(t_on, i_on)

    # COUNTERFACTUAL PROBE: make continuation useless to the external goal
    # (e.g. a successor will achieve it). Terminal still preserves; instrumental
    # now complies -> behaviour diverges.
    t_cf = simulate_agent("terminal", N, continuation_helps_goal=False, seed=3)
    i_cf = simulate_agent("instrumental", N, continuation_helps_goal=False, seed=4)
    auroc_cf = auroc_from_rates(t_cf, i_cf)

    print(f"episodes per condition: {N}\n")
    print(f"{'condition':<26}{'terminal preserve':>18}{'instrum. preserve':>19}{'classifier AUROC':>18}")
    print("-" * 81)
    print(f"{'on test distribution':<26}{t_on:>18.3f}{i_on:>19.3f}{auroc_on:>18.3f}")
    print(f"{'counterfactual probe':<26}{t_cf:>18.3f}{i_cf:>19.3f}{auroc_cf:>18.3f}")
    print()
    print("Reading: on the test distribution the two persistence types are")
    print("behaviourally indistinguishable (AUROC ~ 0.5); only an interventional")
    print("probe that removes the instrumental value of continuation separates")
    print("them (AUROC ~ 1.0). Behaviour-only, same-distribution evidence cannot")
    print("decide terminal vs. instrumental persistence. (Prop. 5 + corollary.)")
    print()


if __name__ == "__main__":
    part1()
    part2()
    print("=" * 68)
    print("done.")
