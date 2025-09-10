import pytest
import os
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test the health endpoint returns 200 and 'ok'."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'ok'


def test_config_value_default(client):
    """Test config endpoint returns default value when MY_CONFIG is not set."""
    # Ensure MY_CONFIG is not set for this test
    if 'MY_CONFIG' in os.environ:
        del os.environ['MY_CONFIG']
    
    response = client.get('/config-value')
    assert response.status_code == 200
    assert response.get_json() == {'config': 'default_value'}


def test_config_value_custom(client):
    """Test config endpoint returns custom value when MY_CONFIG is set."""
    # Set a custom value for this test
    os.environ['MY_CONFIG'] = 'test_config_value'
    
    response = client.get('/config-value')
    assert response.status_code == 200
    assert response.get_json() == {'config': 'test_config_value'}
    
    # Clean up
    del os.environ['MY_CONFIG']


def test_config_value_json_content_type(client):
    """Test config endpoint returns JSON content type."""
    response = client.get('/config-value')
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_nonexistent_endpoint(client):
    """Test that non-existent endpoints return 404."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
