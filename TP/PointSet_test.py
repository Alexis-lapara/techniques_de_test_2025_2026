import struct
import pytest

from encoding import encode_pointset, decode_pointset


def test_encode_pointset_empty():
    data = encode_pointset([])
    # 4 bytes => 0 points
    assert data == struct.pack("<I", 0)


def test_encode_pointset_single_point():
    pointset = [(1.5, -2.0)]
    data = encode_pointset(pointset)

    expected = struct.pack("<Iff", 1, 1.5, -2.0)
    assert data == expected


def test_encode_pointset_multiple_points():
    pointset = [(0., 0.), (1., 1.)]
    data = encode_pointset(pointset)

    expected = struct.pack("<Iffff", 2, 0., 0., 1., 1.)
    assert data == expected


def test_decode_pointset_empty():
    data = struct.pack("<I", 0)
    assert decode_pointset(data) == []


def test_decode_pointset_multiple():
    data = struct.pack("<Iffff", 2, 0., 1., 2., 3.)
    points = decode_pointset(data)

    assert points == [(0., 1.), (2., 3.)]


def test_decode_pointset_invalid_length():
    data = struct.pack("<Iff", 1, 1.0, 2.0)[:-1] 

    with pytest.raises(ValueError):
        decode_pointset(data)
