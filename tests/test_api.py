import pytest
import sys
sys.path.insert(0, 'backend')
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_predict_no_file(client):
    response = client.post('/predict')
    assert response.status_code == 400

def test_predict_invalid_file(client):
    data = {'file': (b'not an image', 'test.txt')}
    response = client.post('/predict', data=data, content_type='multipart/form-data')
    assert response.status_code in [400, 415]
