import pytest
import requests
from unittest.mock import patch, Mock
import json

class TestJokeEndpoint:
    """Test cases for GET /joke/{category} endpoint"""
    
    def test_get_joke_success(self, client):
        """Test successful retrieval of a joke from a valid category"""
        mock_joke_response = {
            "categories": ["dev"],
            "created_at": "2020-01-05 13:42:23.240175",
            "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
            "id": "abc123",
            "updated_at": "2020-01-05 13:42:23.240175",
            "url": "https://api.chucknorris.io/jokes/abc123",
            "value": "Chuck Norris can write infinite recursion functions and have them finish."
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_joke_response
            mock_get.return_value = mock_response
            
            response = client.get('/joke/dev')
            
            assert response.status_code == 200
            assert response.headers['content-type'] == 'application/json'
            
            data = response.get_json()
            assert 'id' in data
            assert 'url' in data
            assert 'value' in data
            assert data['id'] == 'abc123'
            assert data['url'] == 'https://api.chucknorris.io/jokes/abc123'
            assert data['value'] == 'Chuck Norris can write infinite recursion functions and have them finish.'
            
            # Verify the external API was called correctly
            mock_get.assert_called_once_with('https://api.chucknorris.io/jokes/random?category=dev')
    
    def test_get_joke_invalid_category(self, client):
        """Test handling of invalid category"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.json.return_value = {"error": "Category not found"}
            mock_get.return_value = mock_response
            
            response = client.get('/joke/invalid_category')
            
            assert response.status_code == 404
            data = response.get_json()
            assert 'error' in data
            assert 'Category not found' in data['error']
    
    def test_get_joke_external_api_failure(self, client):
        """Test handling when external API fails"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_get.return_value = mock_response
            
            response = client.get('/joke/dev')
            
            assert response.status_code == 503
            data = response.get_json()
            assert 'error' in data
            assert 'Unable to fetch joke' in data['error']
    
    def test_get_joke_external_api_timeout(self, client):
        """Test handling when external API times out"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout()
            
            response = client.get('/joke/dev')
            
            assert response.status_code == 503
            data = response.get_json()
            assert 'error' in data
            assert 'timeout' in data['error'].lower()
    
    def test_get_joke_external_api_connection_error(self, client):
        """Test handling when external API is unreachable"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError()
            
            response = client.get('/joke/dev')
            
            assert response.status_code == 503
            data = response.get_json()
            assert 'error' in data
            assert 'connection' in data['error'].lower()
    
    def test_get_joke_invalid_json_response(self, client):
        """Test handling when external API returns invalid JSON"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_get.return_value = mock_response
            
            response = client.get('/joke/dev')
            
            assert response.status_code == 503
            data = response.get_json()
            assert 'error' in data
            assert 'Invalid response' in data['error']
    
    def test_get_joke_missing_required_fields(self, client):
        """Test handling when external API response is missing required fields"""
        mock_joke_response = {
            "categories": ["dev"],
            "created_at": "2020-01-05 13:42:23.240175",
            # Missing id, url, and value fields
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_joke_response
            mock_get.return_value = mock_response
            
            response = client.get('/joke/dev')
            
            assert response.status_code == 503
            data = response.get_json()
            assert 'error' in data
            assert 'Invalid response format' in data['error']
    
    def test_get_joke_method_not_allowed(self, client):
        """Test that POST method is not allowed"""
        response = client.post('/joke/dev')
        assert response.status_code == 405
    
    def test_get_joke_put_method_not_allowed(self, client):
        """Test that PUT method is not allowed"""
        response = client.put('/joke/dev')
        assert response.status_code == 405
    
    def test_get_joke_delete_method_not_allowed(self, client):
        """Test that DELETE method is not allowed"""
        response = client.delete('/joke/dev')
        assert response.status_code == 405
    
    def test_get_joke_with_special_characters_in_category(self, client):
        """Test handling of category with special characters"""
        mock_joke_response = {
            "id": "xyz789",
            "url": "https://api.chucknorris.io/jokes/xyz789",
            "value": "Chuck Norris can make a joke about anything."
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_joke_response
            mock_get.return_value = mock_response
            
            response = client.get('/joke/dev%20category')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'id' in data
            assert 'url' in data
            assert 'value' in data
    
    def test_get_joke_with_empty_category(self, client):
        """Test handling of empty category parameter"""
        response = client.get('/joke/')
        assert response.status_code == 404
    
    def test_get_joke_with_multiple_categories(self, client):
        """Test that the endpoint handles multiple category parameters correctly"""
        mock_joke_response = {
            "id": "multi123",
            "url": "https://api.chucknorris.io/jokes/multi123",
            "value": "Chuck Norris can handle multiple categories."
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_joke_response
            mock_get.return_value = mock_response
            
            response = client.get('/joke/dev,movie,sport')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'id' in data
            assert 'url' in data
            assert 'value' in data 