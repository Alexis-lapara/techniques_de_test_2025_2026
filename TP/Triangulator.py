"""Implémentation Python de la triangulation de Delaunay."""

Point = tuple[float, float]
Triangle = tuple[int, int, int]
EPS = 1e-12


def _circumcircle_contains(pt: Point, a: Point, b: Point, c: Point) -> bool:
    """Retourne True si pt est à l'intérieur du cercle circonscrit.

    Le cercle circonscrit est défini par le triangle (a, b, c).
    """
    px, py = pt
    ax, ay = a
    bx, by = b
    cx, cy = c

    d = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < EPS:
        return False

    ax2ay2 = ax * ax + ay * ay
    bx2by2 = bx * bx + by * by
    cx2cy2 = cx * cx + cy * cy

    ux = (ax2ay2 * (by - cy) + bx2by2 * (cy - ay) + cx2cy2 * (ay - by)) / d
    uy = (ax2ay2 * (cx - bx) + bx2by2 * (ax - cx) + cx2cy2 * (bx - ax)) / d

    r2 = (ux - ax) ** 2 + (uy - ay) ** 2
    dist2 = (px - ux) ** 2 + (py - uy) ** 2

    return dist2 < r2 - EPS


def triangulate(points: list[Point]) -> list[Triangle]:
    """Triangule une liste de points selon l'algorithme de Delaunay.

    Parameters
    ----------
    points : list[Point]
        Liste des points à trianguler.

    Returns
    -------
    list[Triangle]
        Liste des triangles sous forme de triplets d'indices dans la liste `points`.
        Aucun triangle ne contient de sommet du super-triangle final.

    """
    n_pts = len(points)
    if n_pts < 3:
        return []

    # Construire un super-triangle englobant tous les points
    xmin = min(p[0] for p in points)
    xmax = max(p[0] for p in points)
    ymin = min(p[1] for p in points)
    ymax = max(p[1] for p in points)
    dx = xmax - xmin
    dy = ymax - ymin
    delta = max(dx, dy) if max(dx, dy) > 0 else 1.0
    R = 10.0 * delta
    xmid = (xmin + xmax) / 2.0
    ymid = (ymin + ymax) / 2.0

    super_pts = [
        (xmid - 2 * R, ymid - R),
        (xmid, ymid + 2 * R),
        (xmid + 2 * R, ymid - R),
    ]

    pts = list(points) + super_pts
    n_total = len(pts)
    super_idx = (n_total - 3, n_total - 2, n_total - 1)

    # Triangulation initiale
    triangles: list[Triangle] = [super_idx]

    # Insertion incrémentale des points
    for i in range(n_pts):
        p = pts[i]
        bad_triangles = []

        # Identifier les triangles dont le cercle circonscrit contient p
        for tri in triangles:
            a_idx, b_idx, c_idx = tri
            if _circumcircle_contains(p, pts[a_idx], pts[b_idx], pts[c_idx]):
                bad_triangles.append(tri)

        # Identifier les arêtes frontières de la cavité
        edge_count = {}
        for tri in bad_triangles:
            edges = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]
            for e in edges:
                key = (e[0], e[1]) if e[0] < e[1] else (e[1], e[0])
                edge_count[key] = edge_count.get(key, 0) + 1

        boundary_edges = [e for e, cnt in edge_count.items() if cnt == 1]

        # Supprimer les triangles invalides
        triangles = [t for t in triangles if t not in bad_triangles]

        # Re-trianguler la cavité
        for e in boundary_edges:
            a, b = e
            triangles.append(tuple(sorted((a, b, i))))

    # Filtrer les triangles contenant un sommet du super-triangle
    final = [
        t for t in triangles
        if super_idx[0] not in t and super_idx[1] not in t and super_idx[2] not in t
    ]

    return final
