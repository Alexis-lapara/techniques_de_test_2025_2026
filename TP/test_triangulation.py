"""Tests unitaires pour la fonction triangulate et _circumcircle_contains."""

import pytest

from TP.Triangulator import _circumcircle_contains, triangulate


def test_triangulate_empty():
    """Teste la triangulation d'une liste vide."""
    assert triangulate([]) == []


def test_triangulate_one_point():
    """Teste la triangulation d'un seul point."""
    assert triangulate([(0., 0.)]) == []


def test_triangulate_two_points():
    """Teste la triangulation de deux points."""
    assert triangulate([(0., 0.), (1., 0.)]) == []


def test_triangulate_three_points():
    """Teste la triangulation de trois points formant un triangle."""
    points = [(0., 0.), (1., 0.), (0., 1.)]
    triangles = triangulate(points)
    assert len(triangles) == 1
    assert set(triangles[0]) == {0, 1, 2}


def test_triangulate_square():
    """Teste la triangulation d'un carré (4 points)."""
    points = [(0., 0.), (1., 0.), (1., 1.), (0., 1.)]
    triangles = triangulate(points)
    assert len(triangles) == 2

    valid = [
        {(0, 1, 2), (0, 2, 3)},
        {(1, 2, 3), (1, 3, 0)},
    ]
    result = {tuple(sorted(t)) for t in triangles}
    assert result in valid


def test_triangulate_known_result():
    """Teste un cas connu avec 5 points."""
    pointset = [
        (0., 0.),
        (2., 0.),
        (3., 1.),
        (1.5, 2.),
        (0., 1.),
    ]
    triangles = triangulate(pointset)
    all_indices = {i for t in triangles for i in t}
    assert all_indices == set(range(len(pointset)))

    for i, p in enumerate(pointset):
        for t in triangles:
            if i not in t:
                a, b, c = (pointset[j] for j in t)
                assert not _circumcircle_contains(
                    p, a, b, c
                ), f"Point {p} est à l'intérieur d'un cercle circonscrit incorrect"


def test_triangulate_valid_indices():
    """Vérifie que tous les indices des triangles sont valides."""
    points = [(0., 0.), (1., 0.), (1., 1.), (0., 1.)]
    triangles = triangulate(points)
    for tri in triangles:
        assert len(tri) == 3
        for idx in tri:
            assert isinstance(idx, int)
            assert 0 <= idx < len(points)


def triangle_area(a, b, c):
    """Renvoie l'aire d'un triangle."""
    return abs(
        (b[0] - a[0]) * (c[1] - a[1])
        - (b[1] - a[1]) * (c[0] - a[0])
    ) / 2


def test_triangulate_no_degenerate_triangles():
    """Vérifie que la triangulation ne génère pas de triangles dégénérés."""
    points = [(0., 0.), (2., 0.), (2., 2.), (0., 2.)]
    triangles = triangulate(points)
    for i, j, k in triangles:
        assert triangle_area(points[i], points[j], points[k]) > 1e-12


def test_triangulate_colinear_points():
    """Teste la triangulation de points colinéaires."""
    points = [(0., 0.), (1., 0.), (2., 0.), (3., 0.)]
    triangles = triangulate(points)
    assert triangles == []


def test_triangulate_invalid_point_format():
    """Teste la gestion des points au format invalide."""
    points = [(0, 0), (1, 0), "invalid", (0, 1)]
    with pytest.raises(TypeError):
        triangulate(points)


def test_triangulate_invalid_point_type():
    """Teste la gestion des types de points incorrects."""
    points = [(0, 0), (1, "x"), (0, 1)]
    with pytest.raises(TypeError):
        triangulate(points)
