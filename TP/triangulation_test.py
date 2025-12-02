import pytest
from Triangulator import triangulate

# on considere que la fonction triangulate renvoie une liste de triangles sous forme de tuples d'indices de points
def test_triangulate_empty():
    assert triangulate([]) == []


def test_triangulate_one_point():
    assert triangulate([(0., 0.)]) == []


def test_triangulate_two_points():
    assert triangulate([(0., 0.), (1., 0.)]) == []


def test_triangulate_three_points():
    points = [(0., 0.), (1., 0.), (0., 1.)]
    triangles = triangulate(points)

    assert len(triangles) == 1
    assert set(triangles[0]) == {0, 1, 2}


def test_triangulate_square():
    points = [(0., 0.), (1., 0.), (1., 1.), (0., 1.)]
    triangles = triangulate(points)

    assert len(triangles) == 2

    valid = [
        {(0, 1, 2), (0, 2, 3)},
        {(1, 2, 3), (1, 3, 0)},
    ]
    #on trie les tuples pour éviter les différences d'ordre 
    result = {tuple(sorted(t)) for t in triangles}
    assert result in valid

#test basique avec n-2 triangles n=nbpoints
def test_triangulate_known_result():
    PointSet = [
        (0., 0.),  
        (2., 0.),   
        (3., 1.),   
        (1.5, 2.),  
        (0., 1.)    
    ]

    expected = {
        (0, 1, 2),
        (0, 2, 3),
        (0, 3, 4),
    }

    triangles = triangulate(PointSet)

    #on trie les tuples pour éviter les différences d'ordre 
    result = {tuple(sorted(t)) for t in triangles}

    assert result == expected

def test_triangulate_convex_pentagon():
    points = [
        (0., 0.), (1., 0.), (2., 1.), (1., 2.), (0., 1.)
    ]
    triangles = triangulate(points)

    assert len(triangles) == 3


def test_triangulate_concave_shape():
    points = [
        (0, 0), (2, 0), (2, 2), (1, 1), (0, 2)
    ]
    triangles = triangulate(points)

    assert len(triangles) == 3


def test_triangulate_valid_indices():
    points = [(0., 0.), (1., 0.), (1., 1.), (0., 1.)]
    triangles = triangulate(points)

    for tri in triangles:
        assert len(tri) == 3
        for idx in tri:
            assert isinstance(idx, int)
            assert 0 <= idx < len(points)

#fonction pour calculer l'aire d'un triangle pour faire des verifications sur les triangles generes
def triangle_area(a, b, c):
    return abs(
        (b[0] - a[0]) * (c[1] - a[1])
        - (b[1] - a[1]) * (c[0] - a[0])
    ) / 2

#test pour verifier que l'on gere les triangles degeneres
def test_triangulate_no_degenerate_triangles():
    points = [(0., 0.), (2., 0.), (2., 2.), (0., 2.)]
    triangles = triangulate(points)

    for i, j, k in triangles:
        assert triangle_area(points[i], points[j], points[k]) > 1e-12


def test_triangulate_colinear_points():
    points = [(0., 0.), (1., 0.), (2., 0.), (3., 0.)]
    triangles = triangulate(points)

    assert triangles == []

#test negatifs pour verifier la gestion des erreurs
def test_triangulate_invalid_point_format():
    points = [(0, 0), (1, 0), "invalid", (0, 1)]

    with pytest.raises(TypeError):
        triangulate(points)


def test_triangulate_invalid_point_type():
    points = [(0, 0), (1, "x"), (0, 1)]

    with pytest.raises(TypeError):
        triangulate(points)
