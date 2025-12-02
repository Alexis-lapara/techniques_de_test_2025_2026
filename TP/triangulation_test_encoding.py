import struct
import pytest

from Triangulator import (
    encode_triangles,
    decode_triangles,
)


def test_encode_triangles_empty():
    points = [(0., 0.)]
    triangles = []

    data = encode_triangles(points, triangles)

    expected = struct.pack("<IffI", 1, 0., 0., 0) 
    assert data == expected

def test_encode_triangles_empty_points_empty_triangles():
    points = []
    triangles = []
    data = encode_triangles(points, triangles)

    expected = struct.pack("<II", 0, 0) 
    assert data == expected

def test_encode_triangles_multiple():
    points = [(0., 0.), (1., 0.), (0., 1.), (1., 1.)]
    triangles = [(0, 1, 2), (1, 3, 2)]

    data = encode_triangles(points, triangles)

    expected = struct.pack(
        "<IffffffffI" + "III"*2,
        4,
        0., 0., 1., 0., 0., 1., 1., 1.,
        2,
        0, 1, 2,
        1, 3, 2
    )
    assert data == expected

def test_encode_triangles_negative_index():
    points = [(0., 0.), (1., 0.), (0., 1.)]
    triangles = [(-1, 0, 2)]

    with pytest.raises(ValueError):
        encode_triangles(points, triangles)

def test_encode_triangles_extreme_values():
    points = [(float("inf"), float("-inf"))]
    triangles = []

    data = encode_triangles(points, triangles)
    expected = struct.pack("<IffI", 1, float("inf"), float("-inf"), 0)

    assert data == expected

def test_encode_triangles_simple():
    points = [(0., 0.), (1., 0.), (0., 1.)]
    triangles = [(0, 1, 2)]

    data = encode_triangles(points, triangles)

    expected = struct.pack(
        "<IffffffIIII",
        3, 0., 0., 1., 0., 0., 1.,
        1, 0, 1, 2
    )
    assert data == expected


def test_decode_triangles_simple():
    data = struct.pack(
        "<IffffffIIII",
        3, 0., 0., 1., 0., 0., 1.,
        1, 0, 1, 2
    )

    points, triangles = decode_triangles(data)

    assert points == [(0., 0.), (1., 0.), (0., 1.)]
    assert triangles == [(0, 1, 2)]

def test_decode_triangles_too_short():
    data = b"\x01\x00\x00"  # 3 bytes seulement
    with pytest.raises(ValueError):
        decode_triangles(data)

def test_decode_triangles_header_mismatch_points():
    data = struct.pack("<IffI", 10, 1., 2., 0)  # annonce 10 points mais 2 float seulement
    with pytest.raises(ValueError):
        decode_triangles(data)

def test_decode_triangles_mismatch_triangles():
    data = struct.pack(
        "<IffffffI", 3, 0., 0., 1., 0., 0., 1., 2
    )
    with pytest.raises(ValueError):
        decode_triangles(data)

def test_decode_triangles_multiple():
    data = struct.pack(
        "<IffffffffI" + "III"*2,
        4,
        0., 0., 1., 0., 0., 1., 1., 1.,
        2,
        0, 1, 2,
        1, 3, 2
    )

    points, triangles = decode_triangles(data)

    assert points == [(0., 0.), (1., 0.), (0., 1.), (1., 1.)]
    assert triangles == [(0, 1, 2), (1, 3, 2)]

def test_decode_triangles_invalid_index():
    data = struct.pack(
        "<IffffffIIII",
        3, 0., 0., 1., 0., 0., 1.,
        1, 0, 1, 5  
    )

    with pytest.raises(ValueError):
        decode_triangles(data)

def test_triangles_round_trip_simple():
    pts = [(0., 0.), (1., 0.), (0., 1.)]
    tri = [(0, 1, 2)]

    encoded = encode_triangles(pts, tri)
    decoded_pts, decoded_tri = decode_triangles(encoded)

    assert decoded_pts == pts
    assert decoded_tri == tri

def test_triangles_round_trip_multiple():
    pts = [(0., 0.), (1., 0.), (1., 1.), (0., 1.)]
    tri = [(0, 1, 2), (0, 2, 3)]

    encoded = encode_triangles(pts, tri)
    decoded_pts, decoded_tri = decode_triangles(encoded)

    assert decoded_pts == pts
    assert decoded_tri == tri