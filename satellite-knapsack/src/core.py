"""Shared code for Batch 5 - satellite instrument selection (0/1 knapsack).

Masses are stored as integers in units of 0.1 g (1 kg = 10_000 units) so there
is no floating-point error in feasibility tests. Values and power are integers.
"""
from __future__ import annotations

import heapq
import itertools
import math
from collections import deque
from dataclasses import dataclass

UNITS_PER_KG = 10_000


def kg_to_units(x: float) -> int:
    return round(x * UNITS_PER_KG)


@dataclass(frozen=True)
class Item:
    name: str
    mass: int          # units of 0.1 g
    value: int
    power: int = 0     # watts

    @property
    def kg(self) -> float:
        return self.mass / UNITS_PER_KG

    @property
    def density(self) -> float:      # value per kg
        return self.value / self.kg


_RAW = [("P1", 2.5, 40, 8), ("P2", 3.2, 42, 12), ("P3", 4.8, 60, 10),
        ("P4", 6.1, 72, 15), ("P5", 1.7, 18, 4), ("P6", 5.4, 54, 9)]
INSTANCE = [Item(n, kg_to_units(m), v, p) for n, m, v, p in _RAW]
CAPACITY = kg_to_units(15.0)
POWER_CAP = 35


def sort_by_density(items):
    return sorted(items, key=lambda it: -it.value / it.mass)


def fmt_kg(units: int) -> str:
    return f"{units / UNITS_PER_KG:g}"


def totals(items, names):
    chosen = [it for it in items if it.name in set(names)]
    return (sum(i.value for i in chosen), sum(i.mass for i in chosen),
            sum(i.power for i in chosen))


# --------------------------------------------------------------------------
# Brute force (reference / verification)
# --------------------------------------------------------------------------
def brute_force(items, cap, pcap=None):
    """Return (best_value, [all optimal name-tuples], number_of_feasible_subsets)."""
    n = len(items)
    best, best_sets, feasible = 0, [], 0
    for mask in range(1 << n):
        m = v = p = 0
        for i in range(n):
            if mask >> i & 1:
                m += items[i].mass; v += items[i].value; p += items[i].power
        if m <= cap and (pcap is None or p <= pcap):
            feasible += 1
            names = tuple(items[i].name for i in range(n) if mask >> i & 1)
            if v > best:
                best, best_sets = v, [names]
            elif v == best:
                best_sets.append(names)
    return best, best_sets, feasible


# --------------------------------------------------------------------------
# Greedy by value density
# --------------------------------------------------------------------------
def greedy_density(items, cap, pcap=None, stop_at_first_misfit=True):
    """Pick by value per kg. stop_at_first_misfit=True is the literal
    'until the satellite is full'; False keeps scanning for smaller items."""
    chosen, m, p, v = [], 0, 0, 0
    for it in sorted(items, key=lambda it: -it.value / it.mass):
        fits = m + it.mass <= cap and (pcap is None or p + it.power <= pcap)
        if fits:
            chosen.append(it.name); m += it.mass; p += it.power; v += it.value
        elif stop_at_first_misfit:
            break
    return tuple(chosen), v, m, p


# --------------------------------------------------------------------------
# Table-based DP (the REJECTED technique for real-valued masses)
# --------------------------------------------------------------------------
def dp_knapsack(items, cap):
    """0/1 knapsack over integer mass units. Returns (best, names, cells)."""
    n = len(items)
    dp = [0] * (cap + 1)
    keep = [bytearray(cap + 1) for _ in range(n)]
    for i, it in enumerate(items):
        w, val = it.mass, it.value
        row = keep[i]
        for j in range(cap, w - 1, -1):
            cand = dp[j - w] + val
            if cand > dp[j]:
                dp[j] = cand
                row[j] = 1
    j, names = cap, []
    for i in range(n - 1, -1, -1):
        if keep[i][j]:
            names.append(items[i].name)
            j -= items[i].mass
    return dp[cap], tuple(reversed(names)), (n + 1) * (cap + 1)


# --------------------------------------------------------------------------
# Plain backtracking, no bound (second REJECTED alternative, used for timing)
# --------------------------------------------------------------------------
def backtracking(items, cap, pcap=None):
    n = len(items)
    best = 0
    nodes = 0

    def rec(i, v, m, p):
        nonlocal best, nodes
        nodes += 1
        if v > best:
            best = v
        if i == n:
            return
        it = items[i]
        if m + it.mass <= cap and (pcap is None or p + it.power <= pcap):
            rec(i + 1, v + it.value, m + it.mass, p + it.power)
        rec(i + 1, v, m, p)

    rec(0, 0, 0, 0)
    return best, nodes


# --------------------------------------------------------------------------
# Branch and bound with fractional (LP-relaxation) bound
# --------------------------------------------------------------------------
def branch_and_bound(items, cap, pcap=None, strategy="best", trace=False):
    """Exact 0/1 knapsack by branch and bound.

    items     : list, decided in the given order (pass sort_by_density(...)).
    strategy  : "dfs" (stack), "bfs" (queue) or "best" (priority queue on bound).
    pcap      : optional second capacity (power). The bound is then the MIN of
                the mass-relaxation and the power-relaxation (both valid).
    Returns dict with best value, one optimal set, statistics and optional log.
    """
    items = list(items)
    n = len(items)
    mass_order = sorted(range(n), key=lambda i: -items[i].value / items[i].mass)
    pow_order = (sorted(range(n), key=lambda i: -items[i].value / items[i].power)
                 if pcap is not None else None)

    def frac(order, res, level, room):
        total = 0.0
        for i in order:
            if i < level:
                continue
            r = getattr(items[i], res)
            if r <= room:
                room -= r
                total += items[i].value
            else:
                total += items[i].value * room / r
                break
        return total

    def bound(level, v, m, p):
        b = v + frac(mass_order, "mass", level, cap - m)
        if pcap is not None:
            b = min(b, v + frac(pow_order, "power", level, pcap - p))
        return b

    tick = itertools.count()
    if strategy == "dfs":
        frontier = []
        push = lambda nd, b: frontier.append((nd, b))
        pop = frontier.pop
    elif strategy == "bfs":
        frontier = deque()
        push = lambda nd, b: frontier.append((nd, b))
        pop = frontier.popleft
    elif strategy == "best":
        frontier = []
        push = lambda nd, b: heapq.heappush(frontier, (-b, next(tick), nd))

        def pop():
            nb, _, nd = heapq.heappop(frontier)
            return nd, -nb
    else:
        raise ValueError(strategy)

    st = dict(generated=1, expanded=0, pruned=0, infeasible=0, best=0,
              best_set=(), gen_at_best=1, exp_at_best=0, max_frontier=1)
    log = []

    def label(ch):
        return "{" + ",".join(ch) + "}"

    def cannot_beat(b):          # values are integers -> floor is a valid bound
        return math.floor(b + 1e-9) <= st["best"]

    root_b = bound(0, 0, 0, 0)
    push((0, 0, 0, 0, ()), root_b)
    if trace:
        log.append(f"root: bound = {root_b:.2f}")

    while frontier:
        (level, v, m, p, ch), b = pop()
        if cannot_beat(b):
            st["pruned"] += 1
            if trace:
                log.append(f"POP  {label(ch):<18} v={v:<4} bound={b:7.2f} <= best={st['best']} -> PRUNE")
            if strategy == "best":           # heap: everything left is no better
                st["pruned"] += len(frontier)
                if trace:
                    log.append(f"     best-first stop: {len(frontier)} nodes left in heap all have bound <= {st['best']}")
                break
            continue
        st["expanded"] += 1
        if trace:
            log.append(f"POP  {label(ch):<18} v={v:<4} mass={fmt_kg(m):>5} bound={b:7.2f} -> EXPAND item {items[level].name}")
        if level == n:
            continue
        it = items[level]
        children = []
        # include child
        st["generated"] += 1
        nm, npw = m + it.mass, p + it.power
        if nm <= cap and (pcap is None or npw <= pcap):
            nv = v + it.value
            nch = ch + (it.name,)
            if nv > st["best"]:
                st.update(best=nv, best_set=nch, gen_at_best=st["generated"],
                          exp_at_best=st["expanded"])
                if trace:
                    log.append(f"     new incumbent {label(nch)} value {nv}")
            children.append(((level + 1, nv, nm, npw, nch), bound(level + 1, nv, nm, npw), "include"))
        else:
            st["infeasible"] += 1
            if trace:
                log.append(f"     include {it.name}: mass/power limit exceeded -> INFEASIBLE")
        # exclude child
        st["generated"] += 1
        children.append(((level + 1, v, m, p, ch), bound(level + 1, v, m, p), "exclude"))

        to_push = []
        for nd, cb, kind in children:
            if cannot_beat(cb):
                st["pruned"] += 1
                if trace:
                    log.append(f"     {kind} {it.name}: bound={cb:7.2f} <= best={st['best']} -> PRUNE")
            else:
                to_push.append((nd, cb))
                if trace:
                    log.append(f"     {kind} {it.name}: bound={cb:7.2f} -> queued")
        for nd, cb in (reversed(to_push) if strategy == "dfs" else to_push):
            push(nd, cb)
        st["max_frontier"] = max(st["max_frontier"], len(frontier))

    return dict(best=st["best"], best_set=st["best_set"], stats=st, log=log)
