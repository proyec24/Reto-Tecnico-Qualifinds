import pytest
import requests
import time
from unittest.mock import patch, Mock

class TestIntegration:
    """Integration tests for the complete application flow"""
    
    def test_categories_to_joke_flow(self, client):
        """Test the complete flow from getting categories to getting a joke"""
        # First, get categories
        with patch('requests.get') as mock_get:
            # Mock categories response
            mock_categories_response = Mock()
            mock_categories_response.status_code = 200
            mock_categories_response.json.return_value = ["animal", "career", "dev", "movie"]
            
            # Mock joke response
            mock_joke_response = Mock()
            mock_joke_response.status_code = 200
            mock_joke_response.json.return_value = {
                "id": "flow123",
                "url": "https://api.chucknorris.io/jokes/flow123",
                "value": "Chuck Norris can complete integration tests."
            }
            
            mock_get.side_effect = [mock_categories_response, mock_joke_response]
            
            # Get categories
            categories_response = client.get('/categories')
            assert categories_response.status_code == 200
            categories = categories_response.get_json()
            assert isinstance(categories, list)
            assert len(categories) > 0
            
            # Get a joke from one of the categories
            joke_response = client.get(f'/joke/{categories[0]}')
            assert joke_response.status_code == 200
            joke = joke_response.get_json()
            assert 'id' in joke
            assert 'url' in joke
            assert 'value' in joke
    
    def test_search_integration(self, client):
        """Test search functionality integration"""
        with patch('requests.get') as mock_get:
            mock_search_response = Mock()
            mock_search_response.status_code = 200
            mock_search_response.json.return_value = {
                "total": 1,
                "result": [
                    {
                        "id": "search_integration",
                        "url": "https://api.chucknorris.io/jokes/search_integration",
                        "value": "Chuck Norris can integrate search functionality."
                    }
                ]
            }
            mock_get.return_value = mock_search_response
            
            response = client.get('/search?query=integration')
            assert response.status_code == 200
            data = response.get_json()
            assert 'total' in data
            assert 'result' in data
            assert data['total'] == 1
            assert len(data['result']) == 1
    
    def test_error_propagation(self, client):
        """Test that errors from external API are properly propagated"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
            
            # Test categories endpoint
            categories_response = client.get('/categories')
            assert categories_response.status_code == 503
            
            # Test joke endpoint
            joke_response = client.get('/joke/dev')
            assert joke_response.status_code == 503
            
            # Test search endpoint
            search_response = client.get('/search?query=test')
            assert search_response.status_code == 503
    
    def test_response_format_consistency(self, client):
        """Test that all endpoints return consistent JSON format"""
        with patch('requests.get') as mock_get:
            # Mock successful responses
            mock_categories_response = Mock()
            mock_categories_response.status_code = 200
            mock_categories_response.json.return_value = ["dev", "movie"]
            
            mock_joke_response = Mock()
            mock_joke_response.status_code = 200
            mock_joke_response.json.return_value = {
                "id": "format_test",
                "url": "https://api.chucknorris.io/jokes/format_test",
                "value": "Chuck Norris tests response formats."
            }
            
            mock_search_response = Mock()
            mock_search_response.status_code = 200
            mock_search_response.json.return_value = {
                "total": 1,
                "result": [
                    {
                        "id": "search_format",
                        "url": "https://api.chucknorris.io/jokes/search_format",
                        "value": "Chuck Norris formats responses consistently."
                    }
                ]
            }
            
            mock_get.side_effect = [mock_categories_response, mock_joke_response, mock_search_response]
            
            # Test categories endpoint format
            categories_response = client.get('/categories')
            assert categories_response.headers['content-type'] == 'application/json'
            categories_data = categories_response.get_json()
            assert isinstance(categories_data, list)
            
            # Test joke endpoint format
            joke_response = client.get('/joke/dev')
            assert joke_response.headers['content-type'] == 'application/json'
            joke_data = joke_response.get_json()
            assert isinstance(joke_data, dict)
            assert 'id' in joke_data
            assert 'url' in joke_data
            assert 'value' in joke_data
            
            # Test search endpoint format
            search_response = client.get('/search?query=format')
            assert search_response.headers['content-type'] == 'application/json'
            search_data = search_response.get_json()
            assert isinstance(search_data, dict)
            assert 'total' in search_data
            assert 'result' in search_data
    
    def test_performance_under_load(self, client):
        """Test application performance with multiple concurrent requests"""
        with patch('requests.get') as mock_get:
            # Mock responses for multiple requests
            mock_responses = []
            for i in range(10):
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "id": f"perf_test_{i}",
                    "url": f"https://api.chucknorris.io/jokes/perf_test_{i}",
                    "value": f"Chuck Norris can handle performance test {i}."
                }
                mock_responses.append(mock_response)
            
            mock_get.side_effect = mock_responses
            
            # Make multiple concurrent requests
            start_time = time.time()
            responses = []
            for i in range(10):
                response = client.get('/joke/dev')
                responses.append(response)
            
            end_time = time.time()
            
            # All responses should be successful
            for response in responses:
                assert response.status_code == 200
            
            # Performance check (should complete within reasonable time)
            assert end_time - start_time < 5.0  # Should complete within 5 seconds
    
    def test_caching_behavior(self, client):
        """Test that the application handles caching appropriately"""
        with patch('requests.get') as mock_get:
            # Mock the same response for multiple calls
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = ["dev", "movie"]
            mock_get.return_value = mock_response
            
            # Make multiple requests to the same endpoint
            response1 = client.get('/categories')
            response2 = client.get('/categories')
            response3 = client.get('/categories')
            
            # All should return the same data
            data1 = response1.get_json()
            data2 = response2.get_json()
            data3 = response3.get_json()
            
            assert data1 == data2 == data3
            
            # Verify external API was called (no caching at this level)
            assert mock_get.call_count == 3
    
    def test_edge_case_handling(self, client):
        """Test various edge cases and boundary conditions"""
        with patch('requests.get') as mock_get:
            # Test with very long category name
            long_category = "a" * 1000
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.json.return_value = {"error": "Category not found"}
            mock_get.return_value = mock_response
            
            response = client.get(f'/joke/{long_category}')
            assert response.status_code == 404
            
            # Test with special characters in category
            special_category = "dev!@#$%^&*()"
            response = client.get(f'/joke/{special_category}')
            assert response.status_code == 404
            
            # Test with empty search query
            response = client.get('/search?query=')
            assert response.status_code == 400
    
    def test_health_check_endpoint(self, client):
        """Test if there's a health check endpoint (bonus feature)"""
        # This test assumes the application might have a health check endpoint
        response = client.get('/health')
        
        # If health endpoint exists, it should return 200
        # If it doesn't exist, it should return 404
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'status' in data
            assert data['status'] == 'healthy' 