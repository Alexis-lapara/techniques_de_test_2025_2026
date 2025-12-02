import pytest
import uuid
from unittest.mock import patch
from flask import Response

from triangulator_server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

# -----------------------------
# 400 : UUID invalide
# -----------------------------
def test_invalid_uuid(client):
    rv = client.get("/triangulation/invalid-uuid")
    assert rv.status_code == 400
    assert rv.json["code"] == "INVALID_POINTSET_ID"

# -----------------------------
# 500 : Décodage binaire invalide
# -----------------------------
def test_decode_error(client):
    with patch("triangulator_server.decode_pointset", side_effect=Exception("decode fail")):
        rv = client.get(f"/triangulation/{uuid.uuid4()}")
        assert rv.status_code == 500
        assert rv.json["code"] == "INVALID_POINTSET_BINARY"

# -----------------------------
# 500 : Triangulation échouée
# -----------------------------
def test_triangulate_error(client):
    with patch("triangulator_server.triangulate", side_effect=Exception("triangulate fail")):
        rv = client.get(f"/triangulation/{uuid.uuid4()}")
        assert rv.status_code == 500
        assert rv.json["code"] == "TRIANGULATION_FAILED"

# -----------------------------
# 500 : Encodage échoué
# -----------------------------
def test_encode_error(client):
    with patch("triangulator_server.encode_triangles", side_effect=Exception("encode fail")):
        rv = client.get(f"/triangulation/{uuid.uuid4()}")
        assert rv.status_code == 500
        assert rv.json["code"] == "ENCODING_FAILED"

# -----------------------------
# 200 : succès complet
# -----------------------------
def test_success(client):
    rv = client.get(f"/triangulation/{uuid.uuid4()}")
    assert rv.status_code == 200
    # Doit renvoyer un binaire
    assert isinstance(rv.data, bytes)
    assert len(rv.data) > 0

# -----------------------------
# 503 : Erreur PointSetManager
@patch("triangulator_server.fetch_pointset")
def test_pointset_manager_http_error(mock_fetch, client):
    mock_fetch.side_effect = Exception("PointSetManager unreachable")

    rv = client.get(f"/triangulation/{uuid.uuid4()}")

    assert rv.status_code == 503
    assert rv.json["code"] == "POINTSET_MANAGER_ERROR"
    assert "unreachable" in rv.json["message"]

@patch("triangulator_server.fetch_pointset")
def test_pointset_manager_empty_data(mock_fetch, client):
    mock_fetch.return_value = b""  # données vides

    rv = client.get(f"/triangulation/{uuid.uuid4()}")

    assert rv.status_code == 500
    assert rv.json["code"] == "INVALID_POINTSET_BINARY"