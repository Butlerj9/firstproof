#!/usr/bin/env python3
"""Compute nu_O^eff for the canonical V4 Class II case."""
import sys, io
with open("exp3_v4_output.txt", "w", encoding="utf-8") as out:
    sys.stdout = out
    from fractions import Fraction

    # V4 = Z/2 x Z/2
    # Subgroups: 1, H1, H2, H3, G
    # Canonical O: {1 <=_O H1, 1 <=_O H3, H2 <=_O G}
    #
    # For nu_O^eff(L), we need: max over (K <=_O H) in O, over double coset reps g in L\G/H,
    #   of |H:K| / #(L'-orbits on H/K) where L' = L ∩ gHg^{-1}
    #
    # V4 is abelian, so conjugation is trivial: gHg^{-1} = H for all g.
    # Double cosets: L\G/H. For abelian groups, L\G/H = G/(L+H) (additive).
    #
    # V4 elements: {(0,0), (1,0), (0,1), (1,1)} with Z/2 x Z/2 addition
    # H1 = {(0,0),(1,0)}, H2 = {(0,0),(0,1)}, H3 = {(0,0),(1,1)}

    # Admissible pairs in O:
    # (1, H1): |H1:1| = 2
    # (1, H3): |H3:1| = 2
    # (H2, G): |G:H2| = 2

    # nu_O^eff(L) for each L:

    # L = 1: For any (K,H) in O, L' = 1 ∩ H = 1 always.
    #   (1, H1): #(1-orbits on H1/1) = |H1| = 2. ratio = 2/2 = 1.
    #   (1, H3): #(1-orbits on H3/1) = |H3| = 2. ratio = 2/2 = 1.
    #   (H2, G): #(1-orbits on G/H2) = |G/H2| = 2. ratio = 2/2 = 1.
    #   nu_O^eff(1) = 1.
    out.write("nu_O^eff(1) = 1\n")

    # L = H1: V4 abelian, so L' = H1 ∩ H = H1 ∩ H for each (K,H).
    #   (1, H1): L' = H1 ∩ H1 = H1. #(H1-orbits on H1/1) = 1. ratio = 2/1 = 2.
    #   (1, H3): L' = H1 ∩ H3 = 1. #(1-orbits on H3/1) = 2. ratio = 2/2 = 1.
    #   (H2, G): L' = H1 ∩ G = H1. #(H1-orbits on G/H2).
    #     G/H2 = {{(0,0),(0,1)}, {(1,0),(1,1)}}. H1 = {(0,0),(1,0)}.
    #     H1 acts on G/H2: (1,0) + {(0,0),(0,1)} = {(1,0),(1,1)} = other coset.
    #     So H1 acts transitively on G/H2. #orbits = 1. ratio = 2/1 = 2.
    #   nu_O^eff(H1) = 2.
    out.write("nu_O^eff(H1) = 2\n")

    # L = H2: L' = H2 ∩ H for each (K,H).
    #   (1, H1): L' = H2 ∩ H1 = 1. #(1-orbits on H1/1) = 2. ratio = 2/2 = 1.
    #   (1, H3): L' = H2 ∩ H3 = 1. #(1-orbits on H3/1) = 2. ratio = 2/2 = 1.
    #   (H2, G): L' = H2 ∩ G = H2. #(H2-orbits on G/H2).
    #     G/H2 has 2 cosets. H2 acts on G/H2 by left mult: (0,1) + {(0,0),(0,1)} = {(0,1),(0,0)} = same coset.
    #     So H2 fixes every coset. #orbits = 2. ratio = 2/2 = 1.
    #   nu_O^eff(H2) = 1.
    out.write("nu_O^eff(H2) = 1\n")

    # L = H3: L' = H3 ∩ H for each (K,H).
    #   (1, H1): L' = H3 ∩ H1 = 1. #(1-orbits on H1/1) = 2. ratio = 2/2 = 1.
    #   (1, H3): L' = H3 ∩ H3 = H3. #(H3-orbits on H3/1) = 1. ratio = 2/1 = 2.
    #   (H2, G): L' = H3 ∩ G = H3. #(H3-orbits on G/H2).
    #     G/H2 = {{(0,0),(0,1)}, {(1,0),(1,1)}}. H3 = {(0,0),(1,1)}.
    #     (1,1) + {(0,0),(0,1)} = {(1,1),(1,0)} = other coset.
    #     So H3 acts transitively on G/H2. #orbits = 1. ratio = 2/1 = 2.
    #   nu_O^eff(H3) = 2.
    out.write("nu_O^eff(H3) = 2\n")

    # L = G: L' = G ∩ H = H for each (K,H).
    #   (1, H1): L' = G ∩ H1 = H1. #(H1-orbits on H1/1) = 1. ratio = 2/1 = 2.
    #   (1, H3): L' = G ∩ H3 = H3. #(H3-orbits on H3/1) = 1. ratio = 2/1 = 2.
    #   (H2, G): L' = G ∩ G = G. #(G-orbits on G/H2).
    #     G acts transitively on G/H2. #orbits = 1. ratio = 2/1 = 2.
    #   nu_O^eff(G) = 2.
    out.write("nu_O^eff(G) = 2\n")

    out.write("\n--- CHARACTERIZATION TARGET ---\n")
    out.write("E in tau_{>=n}^O iff:\n")
    out.write("  Phi^1(E) is ceil(n/1) = n-connective\n")
    out.write("  Phi^{H1}(E) is ceil(n/2)-connective\n")
    out.write("  Phi^{H2}(E) is ceil(n/1) = n-connective\n")
    out.write("  Phi^{H3}(E) is ceil(n/2)-connective\n")
    out.write("  Phi^G(E) is ceil(n/2)-connective\n")
    out.write("\nNote: H2 needs n-connective (not n/2) because nu_O^eff(H2) = 1.\n")
    out.write("H1 and H3 get n/2 because they have nu_O^eff = 2.\n")
    out.write("G gets n/2 because nu_O^eff(G) = 2.\n")

    out.write("\n--- KEY STRUCTURAL FEATURES ---\n")
    out.write("1. O-cell generators:\n")
    out.write("   At H1: G_+ ^_{H1} S^{k rho_{H1}} with 2k >= n (regular)\n")
    out.write("   At H3: G_+ ^_{H3} S^{k rho_{H3}} with 2k >= n (regular)\n")
    out.write("   At G:  S^{kV} with V=ind_{H2}^G(1), 2k >= n (non-regular)\n")
    out.write("   NO cells at H2 (1 <=_O H2 not in O)\n\n")
    out.write("2. V = ind_{H2}^G(1) = 1 + chi where chi = sign character for G/H2\n")
    out.write("   chi^{H2} = C (trivial, since H2 = ker(chi)), so dim(chi^{H2}) = 1\n")
    out.write("   chi^{H1} = 0 (H1 not in ker(chi)), chi^{H3} = 0 (H3 not in ker(chi))\n")
    out.write("   chi^G = 0\n")
    out.write("   BUT WAIT: V^{H2} has dim 2 (not 1), so bar{V}^{H2} = 1 (not 0)!\n")
    out.write("   This means the geometric triviality lemma does NOT trivialize S^{bar{V}} at H2.\n\n")
    out.write("3. Isotropy separation at G:\n")
    out.write("   EP_{G,+} ^ E -> E -> tilde{EP}_G ^ E\n")
    out.write("   tilde{EP}_G-local part: geom triviality works (bar{V}^G = 0)\n")
    out.write("   Proper part: EP_{G,+} ^ E supported on H1, H2, H3\n\n")
    out.write("4. THE OBSTRUCTION:\n")
    out.write("   For the proper part, need EP_{G,+} ^ E in tau_{>=n}^O.\n")
    out.write("   Phi^{H2}(EP_{G,+} ^ E) = Phi^{H2}(E), which is n-connective (OK).\n")
    out.write("   But we also need to build it from O-cells.\n")
    out.write("   The O-cells at G level are S^{kV}, whose proper part EP ^ S^{kV}\n")
    out.write("   has Phi^{H2} = S^{2k} (since dim(V^{H2})=2), which is only 2k >= n.\n")
    out.write("   So actually... S^{kV} with 2k >= n already has Phi^{H2} >= n. This is fine!\n\n")
    out.write("5. REVISED ANALYSIS:\n")
    out.write("   The proper part lives on the family {1, H1, H2, H3}.\n")
    out.write("   At H1: Phi^{H1}(EP ^ E) = Phi^{H1}(E), ceil(n/2)-connective\n")
    out.write("   At H2: Phi^{H2}(EP ^ E) = Phi^{H2}(E), n-connective\n")
    out.write("   At H3: Phi^{H3}(EP ^ E) = Phi^{H3}(E), ceil(n/2)-connective\n")
    out.write("   At G: Phi^G(EP ^ E) = 0 (infinitely connective)\n\n")
    out.write("   Need: EP_{G,+} ^ E in tau_{>=n}^O.\n")
    out.write("   tau_{>=n}^O restricted to proper part: generated by\n")
    out.write("     G_+ ^_{H1} S^{k rho_{H1}} (proper part thereof) and\n")
    out.write("     G_+ ^_{H3} S^{k rho_{H3}} (proper part thereof) and\n")
    out.write("     EP ^ S^{kV} (proper part of G-level cells)\n")

sys.stderr.write("Done. Output in exp3_v4_output.txt\n")
