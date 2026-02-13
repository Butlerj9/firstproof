#!/usr/bin/env python3
"""Extract V4 = Z/2 x Z/2 Class II (non-uniform) transfer systems for Session 21."""
import sys, io, os

# Redirect to file to avoid stdout issues
with open("exp2_v4_output.txt", "w", encoding="utf-8") as out:
    # Import after stdout setup
    old_stdout = sys.stdout
    # Suppress exp1 stdout manipulation by pre-setting
    sys.stdout = out

    # Manually set up V4 without importing (avoids stdout closure issue)
    from fractions import Fraction
    from itertools import combinations
    from collections import defaultdict

    # ---- Inline minimal group infrastructure ----
    class PG:
        def __init__(self, name, deg, gens):
            self.name = name
            self.degree = deg
            self.generators = gens
            self._elements = None
            self._subgroups = None
        def identity(self): return tuple(range(self.degree))
        def compose(self, a, b): return tuple(a[b[i]] for i in range(self.degree))
        def inverse(self, a):
            inv = [0]*self.degree
            for i, ai in enumerate(a): inv[ai] = i
            return tuple(inv)
        def conjugate(self, g, h):
            return self.compose(self.compose(g, h), self.inverse(g))
        def elements(self):
            if self._elements: return self._elements
            elts = {self.identity()}
            frontier = list(elts)
            while frontier:
                nf = []
                for g in frontier:
                    for gen in self.generators:
                        for h in [gen, self.inverse(gen)]:
                            p = self.compose(g, h)
                            if p not in elts:
                                elts.add(p); nf.append(p)
                frontier = nf
            self._elements = frozenset(elts)
            return self._elements
        def order(self): return len(self.elements())
        def generate_from(self, gens):
            sub = {self.identity()}
            frontier = [self.identity()]
            for g in gens:
                if g not in sub: sub.add(g); frontier.append(g)
            idx = 0
            while idx < len(frontier):
                g = frontier[idx]; idx += 1
                for gen in gens:
                    for h in [gen, self.inverse(gen)]:
                        p = self.compose(g, h)
                        if p not in sub: sub.add(p); frontier.append(p)
            return frozenset(sub)
        def all_subgroups(self):
            if self._subgroups: return self._subgroups
            elts = list(self.elements())
            subs = set()
            subs.add(frozenset({self.identity()}))
            subs.add(self.elements())
            for e in elts: subs.add(self.generate_from([e]))
            for i, e1 in enumerate(elts):
                for e2 in elts[i:]: subs.add(self.generate_from([e1, e2]))
            self._subgroups = sorted(subs, key=lambda s: (len(s), sorted(s)))
            return self._subgroups
        def conjugate_subgroup(self, H, g):
            ginv = self.inverse(g)
            return frozenset(self.compose(self.compose(g, h), ginv) for h in H)

    # V4
    a = (1, 0, 3, 2); b = (2, 3, 0, 1)
    G = PG("V4", 4, [a, b])
    subs = G.all_subgroups()
    n = len(subs)
    names = {}
    for i, H in enumerate(subs):
        if len(H) == 1: names[i] = "1"
        elif H == G.elements(): names[i] = "G"
        else:
            z2_count = sum(1 for j in range(i+1) if len(subs[j]) == 2)
            names[i] = f"H{z2_count}"

    out.write(f"V4 subgroups: {[(i, names[i], len(subs[i])) for i in range(n)]}\n")

    # Inclusion matrix
    inc = [[subs[i].issubset(subs[j]) for j in range(n)] for i in range(n)]

    # Enumerate transfer systems
    non_reflex = [(i,j) for i in range(n) for j in range(n) if inc[i][j] and i != j]
    m = len(non_reflex)
    out.write(f"Non-reflexive pairs: {m}\n")

    elts = list(G.elements())
    conj_map = {}
    for gi, g in enumerate(elts):
        for si, H in enumerate(subs):
            gHg = G.conjugate_subgroup(H, g)
            for sj, K in enumerate(subs):
                if gHg == K: conj_map[(gi, si)] = sj; break

    inter_idx = {}
    for i in range(n):
        for k in range(n):
            inter = subs[i] & subs[k]
            for j in range(n):
                if subs[j] == inter: inter_idx[(i,k)] = j; break

    reflexive = set((i,i) for i in range(n))
    transfer_systems = []
    for mask in range(1 << m):
        T = set(reflexive)
        for bit in range(m):
            if mask & (1 << bit): T.add(non_reflex[bit])
        ok = True
        for (i,j) in list(T):
            if not ok: break
            for (j2,k) in list(T):
                if j2 == j and (i,k) not in T: ok = False; break
        if not ok: continue
        for gi in range(len(elts)):
            if not ok: break
            for (i,j) in list(T):
                ci = conj_map.get((gi,i)); cj = conj_map.get((gi,j))
                if ci is not None and cj is not None and (ci,cj) not in T: ok = False; break
        if not ok: continue
        for (i,j) in list(T):
            if not ok: break
            for k in range(n):
                if inc[k][j] and k != j:
                    iik = inter_idx.get((i,k))
                    if iik is not None and (iik, k) not in T: ok = False; break
        if not ok: continue
        transfer_systems.append(frozenset(T))
    transfer_systems = list(set(transfer_systems))
    out.write(f"Total transfer systems: {len(transfer_systems)}\n\n")

    # Count orbits function
    def count_orbits(H_elts, K_elts, L_elts):
        H_list = sorted(H_elts); K_set = set(K_elts)
        cosets = []; covered = set()
        for h in H_list:
            c = frozenset(G.compose(h, k) for k in K_set)
            if c not in covered: cosets.append(c); covered.add(c)
        parent = list(range(len(cosets)))
        ct = {c: i for i, c in enumerate(cosets)}
        def find(x):
            while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def union(x, y):
            rx, ry = find(x), find(y)
            if rx != ry: parent[rx] = ry
        for l in L_elts:
            for ci, c in enumerate(cosets):
                rep = next(iter(c))
                img = frozenset(G.compose(G.compose(l, rep), k) for k in K_set)
                cj = ct.get(img)
                if cj is not None: union(ci, cj)
        return len(set(find(i) for i in range(len(cosets))))

    # Classify
    all_pairs = frozenset((i,j) for i in range(n) for j in range(n) if inc[i][j])
    class2 = []
    for T in transfer_systems:
        if T == all_pairs or T == frozenset(reflexive): continue
        # Check uniformity
        is_uni = True
        nr = sorted([(i,j) for (i,j) in T if i != j])
        nontrivK = [(i,j) for (i,j) in nr if len(subs[i]) > 1]
        if not nontrivK: continue  # Class Ia, skip

        for (ki, hi) in nr:
            if ki == hi: continue
            idx_HK = len(subs[hi]) // len(subs[ki])
            for li in range(n):
                if subs[li].issubset(subs[hi]):
                    orb = count_orbits(subs[hi], subs[ki], subs[li])
                    expected = Fraction(idx_HK, len(subs[li]))
                    if Fraction(orb) != expected: is_uni = False; break
            if not is_uni: break
        if is_uni: continue  # uniform, not Class II

        class2.append({'pairs': nr, 'nontrivK': nontrivK, 'n_nontrivK': len(nontrivK)})

    class2.sort(key=lambda x: (x['n_nontrivK'], len(x['pairs'])))
    out.write(f"Class II (non-uniform, non-trivial K) systems: {len(class2)}\n")
    out.write("=" * 70 + "\n")

    for idx, s in enumerate(class2):
        out.write(f"\n--- Class II #{idx+1} ({s['n_nontrivK']} non-triv-K pairs, {len(s['pairs'])} total pairs) ---\n")
        for (i,j) in s['pairs']:
            marker = " *CLASS_II*" if len(subs[i]) > 1 else ""
            out.write(f"  {names[i]} <=_O {names[j]}  (|H:K|={len(subs[j])//len(subs[i])}){marker}\n")
        # Fixed-point table for Class II pairs
        for (i,j) in s['nontrivK']:
            out.write(f"  V = ind_{{{names[i]}}}^{{{names[j]}}}(1), dim={len(subs[j])//len(subs[i])}\n")
            for li in range(n):
                if subs[li].issubset(subs[j]):
                    orb = count_orbits(subs[j], subs[i], subs[li])
                    out.write(f"    dim(V^{{{names[li]}}}) = {orb}\n")

    out.write(f"\n{'='*70}\n")
    out.write(f"CANONICAL: Class II #{1}\n")

sys.stderr.write("Done. Output in exp2_v4_output.txt\n")
