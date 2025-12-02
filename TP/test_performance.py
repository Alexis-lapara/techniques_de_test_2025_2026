import pytest
import time
import random

from encoding import (
    encode_pointset,
    decode_pointset,
    encode_triangles,
    decode_triangles,
)
from Triangulator import triangulate


# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def random_points(n):
    return [(random.random(), random.random()) for _ in range(n)]

def random_triangles(k, max_index):
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
    points = random_points(1000)

    start = time.perf_counter()
    data = encode_pointset(points)
    duration = time.perf_counter() - start

    assert len(data) == 4 + len(points) * 8
    assert duration < 0.5   


@pytest.mark.performance
def test_decode_pointset_perf():
    points = random_points(1000)
    binary = encode_pointset(points)

    start = time.perf_counter()
    out = decode_pointset(binary)
    duration = time.perf_counter() - start

    assert out == points
    assert duration < 0.7


@pytest.mark.performance
def test_encode_triangles_perf():
    points = random_points(500)
    triangles = random_triangles(1000, len(points))

    start = time.perf_counter()
    data = encode_triangles(points, triangles)
    duration = time.perf_counter() - start

    assert duration < 1.0


@pytest.mark.performance
def test_decode_triangles_perf():
    points = random_points(500)
    triangles = random_triangles(1000, len(points))
    binary = encode_triangles(points, triangles)

    start = time.perf_counter()
    p2, t2 = decode_triangles(binary)
    duration = time.perf_counter() - start
    assert duration < 1.2


@pytest.mark.performance
def test_triangulate_perf():
    points = random_points(100)
    start = time.perf_counter()
    triangles = triangulate(points)
    duration = time.perf_counter() - start

    assert isinstance(triangles, list)
    assert duration < 2.0   
