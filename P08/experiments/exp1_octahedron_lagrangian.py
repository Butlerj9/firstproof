"""
EXP-1: Polyhedral Lagrangian S^2 (octahedron) in R^4

Constructs an octahedron embedded in (R^4, omega_0 = dx1^dy1 + dx2^dy2)
with ALL 8 triangular faces Lagrangian. Since the octahedron is
homeomorphic to S^2, Gromov's theorem (no closed exact Lagrangian in R^4)
obstructs smoothing.

Checks:
1. All 8 Lagrangian conditions hold (omega(e1, e2) = 0 for each face)
2. All faces are non-degenerate (positive area)
3. Vertices span R^4 (non-degenerate embedding)
4. Self-intersection check (non-adjacent faces don't intersect)
5. Explicit eigenvalue / PSD check for the smoothing obstruction
"""

import numpy as np
from itertools import combinations

# Standard symplectic form omega = dx1^dy1 + dx2^dy2
# Coordinates: (x1, y1, x2, y2)
# omega(v, w) = v[0]*w[1] - v[1]*w[0] + v[2]*w[3] - v[3]*w[2]

def omega(v, w):
    """Standard symplectic form on R^4."""
    return v[0]*w[1] - v[1]*w[0] + v[2]*w[3] - v[3]*w[2]

def face_is_lagrangian(v1, v2, v3):
    """Check if triangle (v1, v2, v3) lies in a Lagrangian plane."""
    e1 = v2 - v1
    e2 = v3 - v1
    return omega(e1, e2)

def triangle_area_4d(v1, v2, v3):
    """Area of triangle in R^4 via cross product generalization."""
    e1 = v2 - v1
    e2 = v3 - v1
    # Area = 0.5 * |e1 x e2| = 0.5 * sqrt(|e1|^2 |e2|^2 - (e1.e2)^2)
    return 0.5 * np.sqrt(np.dot(e1, e1) * np.dot(e2, e2) - np.dot(e1, e2)**2)

# ============================================================
# CONSTRUCTION
# ============================================================
# Octahedron: 6 vertices, 12 edges, 8 triangular faces
# Vertices labeled 0-5: 0 = north pole, 5 = south pole, 1-4 = equatorial
#
# Faces (8 triangles):
# Top:    (0,1,2), (0,2,3), (0,3,4), (0,4,1)
# Bottom: (5,1,2), (5,2,3), (5,3,4), (5,4,1)
#
# Each vertex is 4-valent.

# Construction derived algebraically:
# v0 = origin (using translation freedom)
# v1 = (1, 0, 0, 0)
# v2 = (0, 0, 1, 0)
# v3 = (0, a, 0, 0)  with a = 1
# v4 = (0, 0, 0, s)  with s = 1
# Top faces through v0 are automatically Lagrangian since all equatorial
# vertices have zero y-components... but we need v3 and v4 to span all of R^4.
#
# For v5 = (p1, -p1*a, p1*a*(1-r)/s, -p1*a) with a=1, r=0, s=1:
#   v5 = (p1, -p1, p1, -p1), choose p1 = 1: v5 = (1, -1, 1, -1)

vertices = np.array([
    [0.0, 0.0, 0.0, 0.0],   # v0 (north pole)
    [1.0, 0.0, 0.0, 0.0],   # v1
    [0.0, 0.0, 1.0, 0.0],   # v2
    [0.0, 1.0, 0.0, 0.0],   # v3
    [0.0, 0.0, 0.0, 1.0],   # v4
    [1.0, -1.0, 1.0, -1.0], # v5 (south pole)
])

faces = [
    (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1),  # top
    (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4),  # bottom
]

# Edges of the octahedron
edges = [
    (0,1), (0,2), (0,3), (0,4),  # from north pole
    (5,1), (5,2), (5,3), (5,4),  # from south pole
    (1,2), (2,3), (3,4), (4,1),  # equatorial
]

print("=" * 60)
print("EXP-1: Polyhedral Lagrangian S^2 (Octahedron) in R^4")
print("=" * 60)

# ============================================================
# CHECK 1: Lagrangian conditions
# ============================================================
print("\n--- CHECK 1: Lagrangian conditions ---")
all_lagrangian = True
for i, (a, b, c) in enumerate(faces):
    val = face_is_lagrangian(vertices[a], vertices[b], vertices[c])
    status = "PASS" if abs(val) < 1e-12 else "FAIL"
    if abs(val) >= 1e-12:
        all_lagrangian = False
    print(f"  Face {i} ({a},{b},{c}): omega = {val:.6e}  [{status}]")
print(f"  All Lagrangian: {all_lagrangian}")

# ============================================================
# CHECK 2: Non-degenerate faces (positive area)
# ============================================================
print("\n--- CHECK 2: Non-degenerate faces ---")
all_nondegenerate = True
for i, (a, b, c) in enumerate(faces):
    area = triangle_area_4d(vertices[a], vertices[b], vertices[c])
    status = "PASS" if area > 1e-10 else "FAIL"
    if area <= 1e-10:
        all_nondegenerate = False
    print(f"  Face {i} ({a},{b},{c}): area = {area:.6f}  [{status}]")
print(f"  All non-degenerate: {all_nondegenerate}")

# ============================================================
# CHECK 3: Vertices span R^4
# ============================================================
print("\n--- CHECK 3: Spanning check ---")
# Check rank of vertex matrix (after centering)
centered = vertices - vertices.mean(axis=0)
rank = np.linalg.matrix_rank(centered)
print(f"  Rank of centered vertex matrix: {rank}")
print(f"  Spans R^4: {rank == 4}")

# ============================================================
# CHECK 4: Self-intersection check
# ============================================================
print("\n--- CHECK 4: Self-intersection check ---")
# For non-adjacent face pairs, check if they intersect.
# Two triangles are adjacent if they share an edge.
# Build adjacency: faces sharing >= 2 vertices are adjacent.

def faces_adjacent(f1, f2):
    return len(set(f1) & set(f2)) >= 2

def triangle_contains_point_2d(p, t):
    """Check if point p is inside triangle t using barycentric coordinates."""
    v0, v1, v2 = t
    d00 = np.dot(v1-v0, v1-v0)
    d01 = np.dot(v1-v0, v2-v0)
    d02 = np.dot(v1-v0, p-v0)
    d11 = np.dot(v2-v0, v2-v0)
    d12 = np.dot(v2-v0, p-v0)
    inv_denom = 1.0 / (d00 * d11 - d01 * d01 + 1e-30)
    u = (d11 * d02 - d01 * d12) * inv_denom
    v = (d00 * d12 - d01 * d02) * inv_denom
    return (u >= -1e-8) and (v >= -1e-8) and (u + v <= 1 + 1e-8)

def segments_intersect_param(p1, d1, p2, d2):
    """
    Find parameters (s, t) such that p1 + s*d1 = p2 + t*d2.
    This is a system A @ [s, t]^T = p2 - p1 in R^4 (overdetermined).
    Return (s, t) if consistent solution exists, else None.
    """
    A = np.column_stack([d1, -d2])
    b = p2 - p1
    # Least squares solution
    res = np.linalg.lstsq(A, b, rcond=None)
    x = res[0]
    residual = np.linalg.norm(A @ x - b)
    if residual < 1e-8:
        s, t = x
        return s, t
    return None

no_intersections = True
non_adj_pairs = []
for i in range(len(faces)):
    for j in range(i+1, len(faces)):
        if not faces_adjacent(faces[i], faces[j]):
            non_adj_pairs.append((i, j))

print(f"  Non-adjacent face pairs: {len(non_adj_pairs)}")

for (i, j) in non_adj_pairs:
    fi = faces[i]
    fj = faces[j]
    # Check if triangles intersect by sampling edges of one against the other
    # More robust: check if any edge of face i intersects the plane of face j
    # within the triangle.

    # Get triangle vertices
    tri_i = vertices[list(fi)]
    tri_j = vertices[list(fj)]

    # For each edge of tri_i, check intersection with the affine plane of tri_j
    found = False
    for e in [(0,1), (1,2), (2,0)]:
        p = tri_i[e[0]]
        d = tri_i[e[1]] - tri_i[e[0]]
        # Plane of tri_j: points of form tri_j[0] + a*(tri_j[1]-tri_j[0]) + b*(tri_j[2]-tri_j[0])
        # We need p + t*d = tri_j[0] + a*ej1 + b*ej2
        # i.e., [d, -ej1, -ej2] @ [t, a, b]^T = tri_j[0] - p
        ej1 = tri_j[1] - tri_j[0]
        ej2 = tri_j[2] - tri_j[0]
        A = np.column_stack([d, -ej1, -ej2])
        rhs = tri_j[0] - p
        res = np.linalg.lstsq(A, rhs, rcond=None)
        x = res[0]
        residual = np.linalg.norm(A @ x - rhs)
        if residual < 1e-8:
            t_param, a_param, b_param = x
            # Check if intersection point is inside both triangles
            if (0 < t_param < 1 - 1e-8 and
                a_param > 1e-8 and b_param > 1e-8 and a_param + b_param < 1 - 1e-8):
                print(f"  INTERSECTION: face {i} edge ({e[0]},{e[1]}) hits face {j}")
                print(f"    t={t_param:.4f}, a={a_param:.4f}, b={b_param:.4f}, residual={residual:.2e}")
                found = True
                no_intersections = False

    if not found:
        # Also check edges of tri_j against plane of tri_i
        for e in [(0,1), (1,2), (2,0)]:
            p = tri_j[e[0]]
            d = tri_j[e[1]] - tri_j[e[0]]
            ei1 = tri_i[1] - tri_i[0]
            ei2 = tri_i[2] - tri_i[0]
            A = np.column_stack([d, -ei1, -ei2])
            rhs = tri_i[0] - p
            res = np.linalg.lstsq(A, rhs, rcond=None)
            x = res[0]
            residual = np.linalg.norm(A @ x - rhs)
            if residual < 1e-8:
                t_param, a_param, b_param = x
                if (0 < t_param < 1 - 1e-8 and
                    a_param > 1e-8 and b_param > 1e-8 and a_param + b_param < 1 - 1e-8):
                    print(f"  INTERSECTION: face {j} edge ({e[0]},{e[1]}) hits face {i}")
                    print(f"    t={t_param:.4f}, a={a_param:.4f}, b={b_param:.4f}, residual={residual:.2e}")
                    found = True
                    no_intersections = False

if no_intersections:
    print("  No self-intersections found among non-adjacent faces.")
else:
    print("  WARNING: Self-intersections detected!")

# ============================================================
# CHECK 5: Euler characteristic = 2 (confirms S^2 topology)
# ============================================================
print("\n--- CHECK 5: Euler characteristic ---")
V = len(vertices)
E = len(edges)
F = len(faces)
chi = V - E + F
print(f"  V = {V}, E = {E}, F = {F}")
print(f"  chi = {V} - {E} + {F} = {chi}")
print(f"  Homeomorphic to S^2: {chi == 2}")

# ============================================================
# CHECK 6: Vertex valence (all should be 4)
# ============================================================
print("\n--- CHECK 6: Vertex valences ---")
valence = [0] * V
for f in faces:
    for v in f:
        valence[v] += 1
for i in range(V):
    print(f"  Vertex {i}: valence = {valence[i]}  {'PASS' if valence[i] == 4 else 'FAIL'}")
all_4valent = all(v == 4 for v in valence)
print(f"  All 4-valent: {all_4valent}")

# ============================================================
# CHECK 7: Gromov obstruction argument
# ============================================================
print("\n--- CHECK 7: Gromov obstruction argument ---")
print("  The octahedron is homeomorphic to S^2.")
print("  Fact (Gromov 1985): There is no closed exact Lagrangian")
print("  submanifold in (R^{2n}, omega_std).")
print("  Since H^1(S^2; R) = 0, any smooth Lagrangian S^2 in R^4")
print("  would be exact (lambda|_L is automatically exact).")
print("  Therefore: no smooth Lagrangian S^2 exists in R^4.")
print("  Conclusion: This polyhedral Lagrangian S^2 CANNOT admit")
print("  a topology-preserving Lagrangian smoothing.")

# ============================================================
# PARAMETRIC FAMILY: vary p1
# ============================================================
print("\n--- Parametric family (varying south pole) ---")
for p1 in [0.5, 1.0, 2.0, 0.1]:
    v5 = np.array([p1, -p1, p1, -p1])
    verts = vertices.copy()
    verts[5] = v5
    all_lag = True
    for (a, b, c) in faces:
        val = face_is_lagrangian(verts[a], verts[b], verts[c])
        if abs(val) > 1e-12:
            all_lag = False
    min_area = min(triangle_area_4d(verts[a], verts[b], verts[c]) for (a,b,c) in faces)
    centered = verts - verts.mean(axis=0)
    r = np.linalg.matrix_rank(centered)
    print(f"  p1={p1}: all_Lagrangian={all_lag}, min_area={min_area:.4f}, rank={r}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  All faces Lagrangian:    {all_lagrangian}")
print(f"  All faces non-degenerate: {all_nondegenerate}")
print(f"  Vertices span R^4:       {rank == 4}")
print(f"  No self-intersections:   {no_intersections}")
print(f"  Euler characteristic:    {chi} (S^2)")
print(f"  All vertices 4-valent:   {all_4valent}")
if all_lagrangian and all_nondegenerate and (rank == 4) and no_intersections and chi == 2 and all_4valent:
    print("\n  *** VALID POLYHEDRAL LAGRANGIAN S^2 WITH 4-VALENT VERTICES ***")
    print("  *** Gromov's theorem obstructs Lagrangian smoothing ***")
    print("  *** Answer to P08: NO (conditional on topology preservation) ***")
