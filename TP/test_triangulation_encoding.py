"""Tests unitaires pour encode_triangles et decode_triangles."""

import struct

import pytest

from TP.encoding import decode_triangles, encode_triangles


def test_encode_triangles_empty():
    """Teste l'encodage d'un triangle vide avec un point."""
    points = [(0., 0.)]
    triangles = []
    data = encode_triangles(points, triangles)
    expected = struct.pack("<IffI", 1, 0., 0., 0)
    assert data == expected


def test_encode_triangles_empty_points_empty_triangles():
    """Teste l'encodage avec points et triangles vides."""
    points = []
    triangles = []
    data = encode_triangles(points, triangles)
    expected = struct.pack("<II", 0, 0)
    assert data == expected


def test_encode_triangles_multiple():
    """Teste l'encodage de plusieurs triangles."""
    points = [(0., 0.), (1., 0.), (0., 1.), (1., 1.)]
    triangles = [(0, 1, 2), (1, 3, 2)]
    data = encode_triangles(points, triangles)
    expected = struct.pack(
        "<IffffffffI" + "III"*2,
        4, 0., 0., 1., 0., 0., 1., 1., 1.,
        2, 0, 1, 2, 1, 3, 2
    )
    assert data == expected


def test_encode_triangles_negative_index():
    """Teste que l'encodage avec un indice négatif lève ValueError."""
    points = [(0., 0.), (1., 0.), (0., 1.)]
    triangles = [(-1, 0, 2)]
    with pytest.raises(ValueError):
        encode_triangles(points, triangles)


def test_encode_triangles_extreme_values():
    """Teste l'encodage avec des valeurs extrêmes (inf et -inf)."""
    points = [(float("inf"), float("-inf"))]
    triangles = []
    data = encode_triangles(points, triangles)
    expected = struct.pack("<IffI", 1, float("inf"), float("-inf"), 0)
    assert data == expected


def test_encode_triangles_simple():
    """Teste l'encodage d'un triangle simple."""
    points = [(0., 0.), (1., 0.), (0., 1.)]
    triangles = [(0, 1, 2)]
    data = encode_triangles(points, triangles)
    expected = struct.pack("<IffffffIIII", 3, 0., 0., 1., 0., 0., 1., 1, 0, 1, 2)
    assert data == expected


def test_decode_triangles_simple():
    """Teste le décodage d'un triangle simple."""
    data = struct.pack("<IffffffIIII", 3, 0., 0., 1., 0., 0., 1., 1, 0, 1, 2)
    points, triangles = decode_triangles(data)
    assert points == [(0., 0.), (1., 0.), (0., 1.)]
    assert triangles == [(0, 1, 2)]


def test_decode_triangles_too_short():
    """Teste le décodage avec des données trop courtes."""
    data = b"\x01\x00\x00"
    with pytest.raises(ValueError):
        decode_triangles(data)


def test_decode_triangles_header_mismatch_points():
    """Teste le décodage avec un header incohérent pour les points."""
    data = struct.pack("<IffI", 10, 1., 2., 0)
    with pytest.raises(ValueError):
        decode_triangles(data)


def test_decode_triangles_mismatch_triangles():
    """Teste le décodage avec un header incohérent pour les triangles."""
    data = struct.pack("<IffffffI", 3, 0., 0., 1., 0., 0., 1., 2)
    with pytest.raises(ValueError):
        decode_triangles(data)


def test_decode_triangles_multiple():
    """Teste le décodage de plusieurs triangles."""
    data = struct.pack("<IffffffffI" + "III"*2,
                       4, 0., 0., 1., 0., 0., 1., 1., 1.,
                       2, 0, 1, 2, 1, 3, 2)
    points, triangles = decode_triangles(data)
    assert points == [(0., 0.), (1., 0.), (0., 1.), (1., 1.)]
    assert triangles == [(0, 1, 2), (1, 3, 2)]


def test_decode_triangles_invalid_index():
    """Teste le décodage avec un indice de triangle invalide."""
    data = struct.pack("<IffffffIIII", 3, 0., 0., 1., 0., 0., 1., 1, 0, 1, 5)
    with pytest.raises(ValueError):
        decode_triangles(data)


def test_triangles_round_trip_simple():
    """Teste un round-trip encode->decode pour un triangle simple."""
    pts = [(0., 0.), (1., 0.), (0., 1.)]
    tri = [(0, 1, 2)]
    encoded = encode_triangles(pts, tri)
    decoded_pts, decoded_tri = decode_triangles(encoded)
    assert decoded_pts == pts
    assert decoded_tri == tri


def test_triangles_round_trip_multiple():
    """Teste un round-trip encode->decode pour plusieurs triangles."""
    pts = [(0., 0.), (1., 0.), (1., 1.), (0., 1.)]
    tri = [(0, 1, 2), (0, 2, 3)]
    encoded = encode_triangles(pts, tri)
    decoded_pts, decoded_tri = decode_triangles(encoded)
    assert decoded_pts == pts
    assert decoded_tri == tri
