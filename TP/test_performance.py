"""Tests de performance pour l'encodage, décodage et triangulation."""
import random
import time

import pytest
from encoding import (
    decode_pointset,
    decode_triangles,
    encode_pointset,
    encode_triangles,
)
from Triangulator import triangulate

# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def random_points(n):
    """Return a list of n random 2D points."""
    return [(random.random(), random.random()) for _ in range(n)]


def random_triangles(k, max_index):
    """Return a list of k random triangles with indices 0..max_index-1."""
    return [
        (
            random.randint(0, max_index - 1),
            random.randint(0, max_index - 1),
            random.randint(0, max_index - 1),
        )
        for _ in range(k)
    ]


# -------------------------------------------------------
# Tests de performance
# -------------------------------------------------------

@pytest.mark.performance
def test_encode_pointset_perf():
    """Measure performance of encode_pointset with 1000 points."""
    points = random_points(1000)

    start = time.perf_counter()
    data = encode_pointset(points)
    duration = time.perf_counter() - start

    assert len(data) == 4 + len(points) * 8
    assert duration < 0.5


@pytest.mark.performance
def test_decode_pointset_perf():
    """Measure performance of decode_pointset with 1000 points."""
    points = random_points(2000)
    binary = encode_pointset(points)

    start = time.perf_counter()
    _ = decode_pointset(binary)
    duration = time.perf_counter() - start
    assert duration < 0.7


@pytest.mark.performance
def test_encode_triangles_perf():
    """Measure performance of encode_triangles with 500 points and 1000 triangles."""
    points = random_points(500)
    triangles = random_triangles(1000, len(points))

    start = time.perf_counter()
    _ = encode_triangles(points, triangles)
    duration = time.perf_counter() - start

    assert duration < 1.0


@pytest.mark.performance
def test_decode_triangles_perf():
    """Measure performance of decode_triangles with 500 points and 1000 triangles."""
    points = random_points(500)
    triangles = random_triangles(1000, len(points))
    binary = encode_triangles(points, triangles)

    start = time.perf_counter()
    _ = decode_triangles(binary)
    duration = time.perf_counter() - start

    assert duration < 0.5


@pytest.mark.performance
def test_triangulate_perf():
    """Measure performance of triangulate with 100 points."""
    points = random_points(100)
    start = time.perf_counter()
    triangles = triangulate(points)
    duration = time.perf_counter() - start

    assert isinstance(triangles, list)
    assert duration < 2.0
