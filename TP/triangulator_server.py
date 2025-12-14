"""Serveur Flask fournissant une API de triangulation de nuages de points.
"""
import uuid

from flask import Flask, Response, jsonify

from TP.encoding import decode_pointset, encode_pointset, encode_triangles
from TP.Triangulator import triangulate

app = Flask(__name__)

# -------------------------------------------------------
# Faux PointSetManager (toujours activé)
# -------------------------------------------------------

def fake_pointset_manager(pointSetId):
    """Renvoie un binaire fixe : 3 points -> un triangle (0,0), (1,0), (0,1)."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    return encode_pointset(points)




def error(code, message, status):
    return jsonify({"code": code, "message": message}), status


# -------------------------------------------------------
# Route principale : GET /triangulation/<pointSetId>
# -------------------------------------------------------

@app.get("/triangulation/<pointSetId>")
def get_triangulation(pointSetId):

    # --------------- Validation de l’UUID ----------------
    try:
        uuid.UUID(pointSetId)
    except ValueError:
        return error("INVALID_POINTSET_ID", "The PointSetID format is invalid.", 400)

    # --------------- FAKE POINTSET MANAGER ---------------
    binary_data = fake_pointset_manager(pointSetId)

    # --------------- Décodage ----------------------------
    try:
        points = decode_pointset(binary_data)
    except Exception:
        return error("INVALID_POINTSET_BINARY",
                     "Could not decode binary PointSet data.",
                     500)

    # --------------- Triangulation -----------------------
    try:
        triangles = triangulate(points)
    except Exception:
        return error("TRIANGULATION_FAILED",
                     "Triangulation computation failed.",
                     500)

    # --------------- Encodage ----------------------------
    try:
        binary_output = encode_triangles(points, triangles)
    except Exception:
        return error("ENCODING_FAILED",
                     "Could not encode the triangulation output.",
                     500)

    # --------------- Réponse OK --------------------------
    return Response(binary_output, mimetype="application/octet-stream")


# -------------------------------------------------------
# Lancement
# -------------------------------------------------------

if __name__ == "__main__":
    print("Triangulator running on http://127.0.0.1:5000")
    print("PointSetManager → FAKE MODE ONLY")
    app.run(host="0.0.0.0", port=5000)
