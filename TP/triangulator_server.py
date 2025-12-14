"""Serveur Flask pour exposer la triangulation de PointSets via HTTP."""

import random
import uuid

from encoding import decode_pointset, encode_pointset, encode_triangles
from flask import Flask, Response, jsonify
from Triangulator import triangulate

app = Flask(__name__)


# -------------------------------------------------------
# Faux PointSetManager (toujours activé)
# -------------------------------------------------------
def fake_pointset_manager(pointSetId: str) -> bytes:
    """Renvoie un PointSet binaire déterministe à partir de l'UUID."""
    try:
        uid = uuid.UUID(pointSetId)
    except ValueError:
        uid = uuid.uuid4()

    seed = uid.int & 0xFFFFFFFF
    rng = random.Random(seed)

    n_points = rng.randint(5, 8)
    points = [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(n_points)]

    return encode_pointset(points)


def fetch_pointset(pointSetId: str) -> bytes:
    """Récupère un PointSet binaire et lève RuntimeError si problème."""
    try:
        data = fake_pointset_manager(pointSetId)
        if not data:
            raise ValueError("Empty PointSet data")
        return data
    except Exception as e:
        raise RuntimeError(f"PointSetManager error: {e}") from e


# -------------------------------------------------------
# Utilitaire d’erreur
# -------------------------------------------------------
def error(code: str, message: str, status: int):
    """Renvoie une réponse JSON d'erreur avec code HTTP."""
    return jsonify({"code": code, "message": message}), status


# -------------------------------------------------------
# Route principale : GET /triangulation/<pointSetId>
# -------------------------------------------------------
@app.get("/triangulation/<pointSetId>")
def get_triangulation(pointSetId: str):
    """Renvoie la triangulation binaire pour un PointSet donné."""
    # --------------- Validation de l’UUID ----------------
    try:
        uuid.UUID(pointSetId)
    except ValueError:
        return error("INVALID_POINTSET_ID", "The PointSetID format is invalid.", 400)

    # --------------- FAKE POINTSET MANAGER ---------------
    try:
        binary_data = fetch_pointset(pointSetId)
    except Exception as e:
        return error("POINTSET_MANAGER_ERROR", str(e), 503)

    # --------------- Décodage ----------------------------
    try:
        points = decode_pointset(binary_data)
    except Exception:
        return error(
            "INVALID_POINTSET_BINARY",
            "Could not decode binary PointSet data.",
            500
        )

    # --------------- Triangulation -----------------------
    try:
        triangles = triangulate(points)
    except Exception:
        return error(
            "TRIANGULATION_FAILED",
            "Triangulation computation failed.",
            500
        )

    # --------------- Encodage ----------------------------
    try:
        binary_output = encode_triangles(points, triangles)
    except Exception:
        return error(
            "ENCODING_FAILED",
            "Could not encode the triangulation output.",
            500
        )

    # --------------- Réponse OK --------------------------
    return Response(binary_output, mimetype="application/octet-stream")


# -------------------------------------------------------
# Lancement
# -------------------------------------------------------
if __name__ == "__main__":
    print("Triangulator running on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)
