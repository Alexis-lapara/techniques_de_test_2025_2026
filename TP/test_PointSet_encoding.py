"""Tests unitaires pour encode_pointset et decode_pointset."""

import math
import struct

import pytest

from TP.encoding import decode_pointset, encode_pointset

# -------------------- Tests d'encodage --------------------


def test_encode_pointset_empty():
    """Test encoding of an empty PointSet."""
    data = encode_pointset([])
    assert data == struct.pack("<I", 0)


def test_encode_pointset_single_point():
    """Test encoding of a PointSet with a single point."""
    pointset = [(1.5, -2.0)]
    data = encode_pointset(pointset)
    expected = struct.pack("<Iff", 1, 1.5, -2.0)
    assert data == expected


def test_encode_pointset_multiple_points():
    """Test encoding of a PointSet with multiple points."""
    pointset = [(0.0, 0.0), (1.0, 1.0)]
    data = encode_pointset(pointset)
    expected = struct.pack("<Iffff", 2, 0.0, 0.0, 1.0, 1.0)
    assert data == expected


def test_encode_pointset_extreme_values():
    """Test encoding of extreme float values (inf, -inf)."""
    pointset = [(float("inf"), float("-inf"))]
    data = encode_pointset(pointset)
    expected = struct.pack("<Iff", 1, float("inf"), float("-inf"))
    assert data == expected


def test_encode_pointset_invalid_type():
    """Test that encoding an invalid PointSet raises TypeError."""
    pointset = [(1, "abc")]
    with pytest.raises(TypeError):
        encode_pointset(pointset)


# -------------------- Tests de décodage --------------------


def test_decode_pointset_empty():
    """Test decoding of an empty PointSet."""
    data = struct.pack("<I", 0)
    assert decode_pointset(data) == []


def test_decode_pointset_multiple():
    """Test decoding of a PointSet with multiple points."""
    data = struct.pack("<Iffff", 2, 0.0, 1.0, 2.0, 3.0)
    points = decode_pointset(data)
    assert points == [(0.0, 1.0), (2.0, 3.0)]


def test_decode_pointset_too_short():
    """Test that decoding a too short PointSet raises ValueError."""
    data = b"\x00\x00\x00"
    with pytest.raises(ValueError):
        decode_pointset(data)


def test_decode_pointset_invalid_length():
    """Test that decoding a truncated PointSet raises ValueError."""
    data = struct.pack("<Iff", 1, 1.0, 2.0)[:-1]
    with pytest.raises(ValueError):
        decode_pointset(data)


def test_decode_pointset_extra_data():
    """Test that decoding a PointSet with inconsistent length raises ValueError."""
    data = struct.pack("<Ifffffff", 3, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0)
    with pytest.raises(ValueError):
        decode_pointset(data)


# -------------------- Test round-trip --------------------


def test_round_trip_simple():
    """Test encode->decode round-trip for a small PointSet."""
    pointset = [(0.5, 1.5), (2.2, 3.3)]
    decoded = decode_pointset(encode_pointset(pointset))
    for (x1, y1), (x2, y2) in zip(pointset, decoded,strict=True):
        assert math.isclose(x1, x2, rel_tol=1e-6)
        assert math.isclose(y1, y2, rel_tol=1e-6)
