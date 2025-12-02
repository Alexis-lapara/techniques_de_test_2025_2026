import struct
import pytest

from triangulator.binary_format import encode_pointset, decode_pointset

#encode tests
def test_encode_pointset_empty():
    data = encode_pointset([])
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
    
def test_encode_pointset_extreme_values():
    pointset = [(float('inf'), float('-inf'))]
    data = encode_pointset(pointset)

    expected = struct.pack("<Iff", 1, float('inf'), float('-inf'))
    assert data == expected

def test_encode_pointset_invalid_type():
    pointset = [(1, "abc")]  
    with pytest.raises(TypeError):
        encode_pointset(pointset)
#decoding tests
def test_decode_pointset_empty():
    data = struct.pack("<I", 0)
    assert decode_pointset(data) == []


def test_decode_pointset_multiple():
    data = struct.pack("<Iffff", 2, 0., 1., 2., 3.)
    points = decode_pointset(data)

    assert points == [(0., 1.), (2., 3.)]


def test_decode_pointset_too_short():
    data = b"\x00\x00\x00"  
    with pytest.raises(ValueError):
        decode_pointset(data)
def test_decode_pointset_invalid_length():
    data = struct.pack("<Iff", 1, 1.0, 2.0)[:-1] 

    with pytest.raises(ValueError):
        decode_pointset(data)

def test_decode_pointset_pluspet():
    data = struct.pack("<Ifffffff", 3, 1., 2., 3., 4., 5., 6.) 
    with pytest.raises(ValueError):
        decode_pointset(data)
#test decode encode 
def test_round_trip_simple():
    pointset = [(0.5, 1.5), (2.2, 3.3)]
    assert decode_pointset(encode_pointset(pointset)) == pointset