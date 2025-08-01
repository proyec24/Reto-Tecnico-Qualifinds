import pytest
import requests
from unittest.mock import patch, Mock

class TestRequirements:
    """Test cases to verify all requirements from the README are met"""
    
    def test_categories_endpoint_requirements(self, client):
        """Test that GET /categories meets all requirements"""
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
            
            # Requirement: Returns a list of joke categories
            assert response.status_code == 200
            data = response.get_json()
            assert isinstance(data, list)
            assert len(data) > 0
            assert all(isinstance(category, str) for category in data)
            
            # Requirement: Internally calls the correct API
            mock_get.assert_called_once_with('https://api.chucknorris.io/jokes/categories')
    
    def test_joke_endpoint_requirements(self, client):
        """Test that GET /joke/{category} meets all requirements"""
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
            
            # Requirement: Returns a random joke from the specified category
            assert response.status_code == 200
            data = response.get_json()
            
            # Requirement: Expected response format
            assert 'id' in data
            assert 'url' in data
            assert 'value' in data
            assert data['id'] == 'abc123'
            assert data['url'] == 'https://api.chucknorris.io/jokes/abc123'
            assert data['value'] == 'Chuck Norris can write infinite recursion functions and have them finish.'
            
            # Requirement: Internally calls the correct API
            mock_get.assert_called_once_with('https://api.chucknorris.io/jokes/random?category=dev')
    
    def test_edge_case_handling_requirement(self, client):
        """Test that edge cases are handled as required"""
        # Test invalid category
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.json.return_value = {"error": "Category not found"}
            mock_get.return_value = mock_response
            
            response = client.get('/joke/invalid_category')
            
            # Requirement: Handle edge cases (e.g. invalid category)
            assert response.status_code == 404
            data = response.get_json()
            assert 'error' in data
            assert 'Category not found' in data['error']
    
    def test_meaningful_http_status_codes_requirement(self, client):
        """Test that meaningful HTTP status codes are returned"""
        # Test 200 for success
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = ["dev", "movie"]
            mock_get.return_value = mock_response
            
            response = client.get('/categories')
            assert response.status_code == 200
        
        # Test 404 for not found
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.json.return_value = {"error": "Category not found"}
            mock_get.return_value = mock_response
            
            response = client.get('/joke/invalid_category')
            assert response.status_code == 404
        
        # Test 503 for service unavailable
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_get.return_value = mock_response
            
            response = client.get('/categories')
            assert response.status_code == 503
        
        # Test 405 for method not allowed
        response = client.post('/categories')
        assert response.status_code == 405
    
    def test_bonus_search_endpoint_requirement(self, client):
        """Test the bonus search endpoint requirement"""
        mock_search_response = {
            "total": 1,
            "result": [
                {
                    "id": "search_bonus",
                    "url": "https://api.chucknorris.io/jokes/search_bonus",
                    "value": "Chuck Norris can implement bonus features."
                }
            ]
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_search_response
            mock_get.return_value = mock_response
            
            response = client.get('/search?query=bonus')
            
            # Bonus requirement: GET /search?query=term endpoint
            assert response.status_code == 200
            data = response.get_json()
            assert 'total' in data
            assert 'result' in data
            
            # Bonus requirement: Uses the correct API
            mock_get.assert_called_once_with('https://api.chucknorris.io/jokes/search?query=bonus')
    
    def test_bonus_category_validation_requirement(self, client):
        """Test the bonus category validation requirement"""
        mock_categories = ["animal", "career", "dev", "movie"]
        
        with patch('requests.get') as mock_get:
            # Mock categories endpoint for validation
            mock_categories_response = Mock()
            mock_categories_response.status_code = 200
            mock_categories_response.json.return_value = mock_categories
            
            # Mock joke endpoint
            mock_joke_response = Mock()
            mock_joke_response.status_code = 200
            mock_joke_response.json.return_value = {
                "id": "validated",
                "url": "https://api.chucknorris.io/jokes/validated",
                "value": "Chuck Norris validates categories."
            }
            
            mock_get.side_effect = [mock_categories_response, mock_joke_response]
            
            response = client.get('/joke/dev')
            
            # Bonus requirement: Validate that the provided category exists
            assert response.status_code == 200
            data = response.get_json()
            assert 'id' in data
            assert 'url' in data
            assert 'value' in data
    
    def test_bonus_input_validation_requirement(self, client):
        """Test the bonus input validation requirement"""
        # Test with potentially malicious input
        response = client.get('/joke/<script>alert("xss")</script>')
        
        # Bonus requirement: Input validation & graceful error handling
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid input' in data['error']
    
    def test_bonus_graceful_error_handling_requirement(self, client):
        """Test the bonus graceful error handling requirement"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
            
            response = client.get('/categories')
            
            # Bonus requirement: Graceful error handling
            assert response.status_code == 503
            data = response.get_json()
            assert 'error' in data
            assert 'Service temporarily unavailable' in data['error']
    
    def test_code_clarity_and_structure_requirement(self, client):
        """Test that the code demonstrates clarity and structure"""
        # This test verifies that the API responses are well-structured
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = ["dev", "movie"]
            mock_get.return_value = mock_response
            
            response = client.get('/categories')
            
            # Requirement: Use clear, clean code (demonstrated by consistent response format)
            assert response.status_code == 200
            assert response.headers['content-type'] == 'application/json'
            data = response.get_json()
            assert isinstance(data, list)
    
    def test_code_reusability_and_modularity_requirement(self, client):
        """Test that the code demonstrates reusability and modularity"""
        # This test verifies that the same patterns are used across endpoints
        with patch('requests.get') as mock_get:
            # Test categories endpoint
            mock_categories_response = Mock()
            mock_categories_response.status_code = 200
            mock_categories_response.json.return_value = ["dev", "movie"]
            
            # Test joke endpoint
            mock_joke_response = Mock()
            mock_joke_response.status_code = 200
            mock_joke_response.json.return_value = {
                "id": "modular",
                "url": "https://api.chucknorris.io/jokes/modular",
                "value": "Chuck Norris writes modular code."
            }
            
            mock_get.side_effect = [mock_categories_response, mock_joke_response]
            
            # Both endpoints should follow similar patterns
            categories_response = client.get('/categories')
            joke_response = client.get('/joke/dev')
            
            # Requirement: Code reusability and modularity (demonstrated by consistent patterns)
            assert categories_response.status_code == 200
            assert joke_response.status_code == 200
            assert categories_response.headers['content-type'] == 'application/json'
            assert joke_response.headers['content-type'] == 'application/json' 