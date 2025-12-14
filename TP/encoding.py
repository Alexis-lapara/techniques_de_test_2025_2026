"""Fonctions d'encodage et de décodage pour les PointSets et triangles."""
import struct

Point = tuple[float, float]
Triangle = tuple[int, int, int]


# -------------------- POINTSET --------------------

def encode_pointset(points: list[Point]) -> bytes:
    """Encode une liste de points en binaire.

    Format: <Iffff...> (nombre de points + coordonnées).

    Parameters
    ----------
    points : list[Point]
        Liste de points à encoder.

    Returns
    -------
    bytes
        Données binaires représentant le PointSet.

    """
    n = len(points)
    data = struct.pack("<I", n)

    for idx, (x, y) in enumerate(points):
        # Vérification des types
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError(f"Coordonnées du point {idx} invalides: ({x}, {y})")

        data += struct.pack("<ff", float(x), float(y))

    return data



def decode_pointset(data: bytes) -> list[Point]:
    """Décode un binaire en liste de points.

    Parameters
    ----------
    data : bytes
        Données binaires représentant un PointSet.

    Returns
    -------
    list[Point]
        Liste de points décodés.

    """
    if len(data) < 4:
        raise ValueError("Données trop courtes pour contenir le nombre de points")

    n_points = struct.unpack("<I", data[:4])[0]
    expected_length = 4 + n_points * 8
    if len(data) != expected_length:
        raise ValueError("Taille de données incohérente avec le nombre de points")

    points = []
    offset = 4
    for _ in range(n_points):
        x, y = struct.unpack("<ff", data[offset:offset + 8])
        points.append((x, y))
        offset += 8
    return points


# -------------------- TRIANGLES --------------------

def encode_triangles(points: list[Point], triangles: list[Triangle]) -> bytes:
    """Encode points et triangles en binaire.

    Format:
        [PointSet binaire] + [nombre de triangles <I>] + [indices triangles].

    Parameters
    ----------
    points : list[Point]
        Liste des points.
    triangles : list[Triangle]
        Liste des triangles (indices).

    Returns
    -------
    bytes
        Données binaires représentant les points et les triangles.

    """
    data = encode_pointset(points)
    n_pts = len(points)
    n_triangles = len(triangles)
    data += struct.pack("<I", n_triangles)
    for a, b, c in triangles:
        if not (0 <= a < n_pts) or not (0 <= b < n_pts) or not (0 <= c < n_pts):
            raise ValueError(f"Triangle {a,b,c} contient un indice invalide")
        data += struct.pack("<III", a, b, c)
    return data


def decode_triangles(data: bytes) -> tuple[list[Point], list[Triangle]]:
    """Décode un binaire en points et triangles.

    Parameters
    ----------
    data : bytes
        Données binaires encodant les points et les triangles.

    Returns
    -------
    tuple[list[Point], list[Triangle]]
        Points et triangles décodés.

    """
    if len(data) < 4:
        raise ValueError("Données trop courtes pour contenir le nombre de points")

    n_points = struct.unpack("<I", data[:4])[0]
    points_length = 4 + n_points * 8
    points_data = data[:points_length]
    points = decode_pointset(points_data)

    if len(data) < points_length + 4:
        n_triangles = 0
        triangles = []
    else:
        n_triangles = struct.unpack("<I", data[points_length:points_length + 4])[0]
        triangles = []
        offset = points_length + 4
        for _ in range(n_triangles):
            if offset + 12 > len(data):
                raise ValueError("Données trop courtes pour triangles")
            a, b, c = struct.unpack("<III", data[offset:offset + 12])
            if a >= n_points or b >= n_points or c >= n_points:
                raise ValueError(f"Indice de triangle hors limites: {(a, b, c)}")
            triangles.append((a, b, c))
            offset += 12

    return points, triangles
