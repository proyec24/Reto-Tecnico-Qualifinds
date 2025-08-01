import pytest
import requests
from unittest.mock import patch, Mock
import json

class TestBonusEndpoints:
    """Test cases for bonus endpoints (optional features)"""
    
    def test_search_jokes_success(self, client):
        """Test successful search for jokes by query term"""
        mock_search_response = {
            "total": 2,
            "result": [
                {
                    "categories": ["dev"],
                    "created_at": "2020-01-05 13:42:23.240175",
                    "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
                    "id": "search1",
                    "updated_at": "2020-01-05 13:42:23.240175",
                    "url": "https://api.chucknorris.io/jokes/search1",
                    "value": "Chuck Norris can write infinite recursion functions and have them finish."
                },
                {
                    "categories": ["dev"],
                    "created_at": "2020-01-05 13:42:23.240175",
                    "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
                    "id": "search2",
                    "updated_at": "2020-01-05 13:42:23.240175",
                    "url": "https://api.chucknorris.io/jokes/search2",
                    "value": "Chuck Norris can debug code with his bare hands."
                }
            ]
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_search_response
            mock_get.return_value = mock_response
            
            response = client.get('/search?query=programming')
            
            assert response.status_code == 200
            assert response.headers['content-type'] == 'application/json'
            
            data = response.get_json()
            assert 'total' in data
            assert 'result' in data
            assert data['total'] == 2
            assert len(data['result']) == 2
            
            # Verify the external API was called correctly
            mock_get.assert_called_once_with('https://api.chucknorris.io/jokes/search?query=programming')
    
    def test_search_jokes_no_results(self, client):
        """Test search with no results"""
        mock_search_response = {
            "total": 0,
            "result": []
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_search_response
            mock_get.return_value = mock_response
            
            response = client.get('/search?query=nonexistent')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['total'] == 0
            assert len(data['result']) == 0
    
    def test_search_jokes_missing_query(self, client):
        """Test search without query parameter"""
        response = client.get('/search')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'query parameter is required' in data['error']
    
    def test_search_jokes_empty_query(self, client):
        """Test search with empty query parameter"""
        response = client.get('/search?query=')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'query parameter cannot be empty' in data['error']
    
    def test_search_jokes_external_api_failure(self, client):
        """Test handling when external search API fails"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_get.return_value = mock_response
            
            response = client.get('/search?query=test')
            
            assert response.status_code == 503
            data = response.get_json()
            assert 'error' in data
            assert 'Unable to search jokes' in data['error']
    
    def test_category_validation_success(self, client):
        """Test that category validation works correctly"""
        # First, mock the categories endpoint to return valid categories
        mock_categories = ["animal", "career", "celebrity", "dev", "explicit", 
                          "fashion", "food", "history", "money", "movie", 
                          "music", "political", "religion", "science", "sport", 
                          "travel"]
        
        # Then mock the joke endpoint
        mock_joke_response = {
            "id": "valid123",
            "url": "https://api.chucknorris.io/jokes/valid123",
            "value": "Chuck Norris can validate categories."
        }
        
        with patch('requests.get') as mock_get:
            # First call to categories endpoint
            mock_categories_response = Mock()
            mock_categories_response.status_code = 200
            mock_categories_response.json.return_value = mock_categories
            
            # Second call to joke endpoint
            mock_joke_response_obj = Mock()
            mock_joke_response_obj.status_code = 200
            mock_joke_response_obj.json.return_value = mock_joke_response
            
            mock_get.side_effect = [mock_categories_response, mock_joke_response_obj]
            
            response = client.get('/joke/dev')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'id' in data
            assert 'url' in data
            assert 'value' in data
    
    def test_category_validation_invalid_category(self, client):
        """Test that invalid categories are properly rejected"""
        mock_categories = ["animal", "career", "celebrity", "dev", "explicit", 
                          "fashion", "food", "history", "money", "movie", 
                          "music", "political", "religion", "science", "sport", 
                          "travel"]
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_categories
            mock_get.return_value = mock_response
            
            response = client.get('/joke/invalid_category')
            
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
            assert 'Invalid category' in data['error']
    
    def test_input_validation_special_characters(self, client):
        """Test input validation with special characters"""
        response = client.get('/joke/<script>alert("xss")</script>')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid input' in data['error']
    
    def test_input_validation_sql_injection(self, client):
        """Test input validation against SQL injection attempts"""
        response = client.get('/joke/1; DROP TABLE jokes; --')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid input' in data['error']
    
    def test_graceful_error_handling_network_error(self, client):
        """Test graceful error handling for network errors"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("Network error")
            
            response = client.get('/joke/dev')
            
            assert response.status_code == 503
            data = response.get_json()
            assert 'error' in data
            assert 'Service temporarily unavailable' in data['error']
    
    def test_graceful_error_handling_rate_limit(self, client):
        """Test graceful error handling for rate limiting"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 429
            mock_response.json.return_value = {"error": "Rate limit exceeded"}
            mock_get.return_value = mock_response
            
            response = client.get('/joke/dev')
            
            assert response.status_code == 429
            data = response.get_json()
            assert 'error' in data
            assert 'Rate limit exceeded' in data['error']
    
    def test_search_jokes_method_not_allowed(self, client):
        """Test that POST method is not allowed for search endpoint"""
        response = client.post('/search?query=test')
        assert response.status_code == 405
    
    def test_search_jokes_put_method_not_allowed(self, client):
        """Test that PUT method is not allowed for search endpoint"""
        response = client.put('/search?query=test')
        assert response.status_code == 405
    
    def test_search_jokes_delete_method_not_allowed(self, client):
        """Test that DELETE method is not allowed for search endpoint"""
        response = client.delete('/search?query=test')
        assert response.status_code == 405 