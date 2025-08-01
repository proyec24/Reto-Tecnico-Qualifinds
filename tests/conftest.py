import pytest
import sys
import os

# Add the parent directory to the Python path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def client():
    """Test client fixture for making requests to the application"""
    # This fixture will be implemented when the actual application is created
    # For now, it's a placeholder that will be updated once the app is built
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_categories():
    """Fixture providing mock categories data"""
    return ["animal", "career", "celebrity", "dev", "explicit", 
            "fashion", "food", "history", "money", "movie", 
            "music", "political", "religion", "science", "sport", 
            "travel"]

@pytest.fixture
def mock_joke_response():
    """Fixture providing mock joke response data"""
    return {
        "categories": ["dev"],
        "created_at": "2020-01-05 13:42:23.240175",
        "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
        "id": "abc123",
        "updated_at": "2020-01-05 13:42:23.240175",
        "url": "https://api.chucknorris.io/jokes/abc123",
        "value": "Chuck Norris can write infinite recursion functions and have them finish."
    }

@pytest.fixture
def mock_search_response():
    """Fixture providing mock search response data"""
    return {
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