import pytest
import requests
from unittest.mock import patch, Mock
import json

class TestCategoriesEndpoint:
    """Test cases for GET /categories endpoint"""
    
    def test_get_categories_success(self, client):
        """Test successful retrieval of categories"""
        # Mock the external API response
        mock_categories = ["animal", "career", "celebrity", "dev", "explicit", 
                          "fashion", "food", "history", "money", "movie", 
                          "music", "political", "religion", "science", "sport", 
                          "travel"]
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_categories
            mock_get.return_value = mock_response
            
            response = client.get('/categories')
            
            assert response.status_code == 200
            assert response.headers['content-type'] == 'application/json'
            
            data = response.get_json()
            assert isinstance(data, list)
            assert len(data) > 0
            assert all(isinstance(category, str) for category in data)
            
            # Verify the external API was called correctly
            mock_get.assert_called_once_with('https://api.chucknorris.io/jokes/categories')
    
    def test_get_categories_external_api_failure(self, client):
        """Test handling when external API fails"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_get.return_value = mock_response
            
            response = client.get('/categories')
            
            assert response.status_code == 503  # Service Unavailable
            data = response.get_json()
            assert 'error' in data
            assert 'Unable to fetch categories' in data['error']
    
    def test_get_categories_external_api_timeout(self, client):
        """Test handling when external API times out"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout()
            
            response = client.get('/categories')
            
            assert response.status_code == 503
            data = response.get_json()
            assert 'error' in data
            assert 'timeout' in data['error'].lower()
    
    def test_get_categories_external_api_connection_error(self, client):
        """Test handling when external API is unreachable"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError()
            
            response = client.get('/categories')
            
            assert response.status_code == 503
            data = response.get_json()
            assert 'error' in data
            assert 'connection' in data['error'].lower()
    
    def test_get_categories_invalid_json_response(self, client):
        """Test handling when external API returns invalid JSON"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_get.return_value = mock_response
            
            response = client.get('/categories')
            
            assert response.status_code == 503
            data = response.get_json()
            assert 'error' in data
            assert 'Invalid response' in data['error']
    
    def test_get_categories_method_not_allowed(self, client):
        """Test that POST method is not allowed"""
        response = client.post('/categories')
        assert response.status_code == 405  # Method Not Allowed
    
    def test_get_categories_put_method_not_allowed(self, client):
        """Test that PUT method is not allowed"""
        response = client.put('/categories')
        assert response.status_code == 405
    
    def test_get_categories_delete_method_not_allowed(self, client):
        """Test that DELETE method is not allowed"""
        response = client.delete('/categories')
        assert response.status_code == 405 