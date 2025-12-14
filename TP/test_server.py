"""Tests pour le serveur Flask de triangulation de PointSets."""
import uuid
from unittest.mock import patch

import pytest
from triangulator_server import app


@pytest.fixture
def client():
    """Renvoie un client de test Flask pour le serveur de triangulation."""
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

# -----------------------------
# 400 : UUID invalide
# -----------------------------
def test_invalid_uuid(client):
    """Renvoie 400 si le PointSetID n'est pas un UUID valide."""
    rv = client.get("/triangulation/invalid-uuid")
    assert rv.status_code == 400
    assert rv.is_json

# -----------------------------
# 500 : Décodage binaire invalide
# -----------------------------
def test_decode_error(client):
    """Renvoie 500 si le décodage du PointSet binaire échoue."""
    with patch(
        "triangulator_server.decode_pointset", 
        side_effect=Exception("échec du décodage")
    ):
        rv = client.get(f"/triangulation/{uuid.uuid4()}")
        assert rv.status_code == 500
        assert rv.is_json

def test_triangulate_error(client):
    """Renvoie 500 si le calcul de la triangulation échoue."""
    with patch(
        "triangulator_server.triangulate", 
        side_effect=Exception("échec de la triangulation")
    ):
        rv = client.get(f"/triangulation/{uuid.uuid4()}")
        assert rv.status_code == 500
        assert rv.is_json

def test_encode_error(client):
    """Renvoie 500 si l'encodage du résultat de triangulation échoue."""
    with patch(
        "triangulator_server.encode_triangles", 
        side_effect=Exception("échec de l'encodage")
    ):
        rv = client.get(f"/triangulation/{uuid.uuid4()}")
        assert rv.status_code == 500
        assert rv.is_json

def test_success(client):
    """Renvoie 200 et les données binaires en cas de triangulation réussie."""
    rv = client.get(f"/triangulation/{uuid.uuid4()}")
    assert rv.status_code == 200
    assert isinstance(rv.data, bytes)
    assert len(rv.data) > 0

@patch("triangulator_server.fetch_pointset")
def test_pointset_manager_http_error(mock_fetch, client):
    """Renvoie 503 si la récupération du PointSet échoue."""
    mock_fetch.side_effect = Exception("PointSetManager inaccessible")
    rv = client.get(f"/triangulation/{uuid.uuid4()}")
    assert rv.status_code == 503
    assert rv.is_json


@patch("triangulator_server.fetch_pointset")
def test_pointset_manager_empty_data(mock_fetch, client):
    """Renvoie 500 si les données récupérées du PointSet sont vides."""
    mock_fetch.return_value = b""
    rv = client.get(f"/triangulation/{uuid.uuid4()}")
    assert rv.status_code == 500
    assert rv.is_json
