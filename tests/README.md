# Test Suite for Chuck Norris API Backend Challenge

This test suite provides comprehensive automated testing for the Chuck Norris API backend challenge, covering all requirements specified in the README.

## Test Structure

### Core Test Files

- **`test_categories_endpoint.py`** - Tests for GET `/categories` endpoint
- **`test_joke_endpoint.py`** - Tests for GET `/joke/{category}` endpoint  
- **`test_bonus_endpoints.py`** - Tests for bonus features (search, validation, etc.)
- **`test_integration.py`** - Integration tests for complete application flow
- **`test_requirements.py`** - Tests that verify all README requirements are met

### Configuration Files

- **`conftest.py`** - Pytest fixtures and configuration
- **`pytest.ini`** - Pytest configuration and markers
- **`requirements-test.txt`** - Test dependencies

## Test Coverage

### Required Endpoints

#### GET `/categories`
- ✅ Returns list of joke categories
- ✅ Internally calls `https://api.chucknorris.io/jokes/categories`
- ✅ Handles external API failures gracefully
- ✅ Returns meaningful HTTP status codes
- ✅ Validates response format

#### GET `/joke/{category}`
- ✅ Returns random joke from specified category
- ✅ Internally calls `https://api.chucknorris.io/jokes/random?category={category}`
- ✅ Returns expected response format with `id`, `url`, and `value`
- ✅ Handles invalid categories
- ✅ Handles external API failures gracefully

### Bonus Features (Optional)

#### GET `/search?query=term`
- ✅ Searches jokes by query term
- ✅ Uses `https://api.chucknorris.io/jokes/search?query=term`
- ✅ Returns total count and results array
- ✅ Handles missing/empty query parameters

#### Category Validation
- ✅ Validates that provided category exists before requesting joke
- ✅ Returns appropriate error for invalid categories

#### Input Validation & Error Handling
- ✅ Validates input against XSS and injection attempts
- ✅ Graceful error handling for network issues
- ✅ Proper HTTP status codes for different error scenarios

## Running the Tests

### Prerequisites

1. Install test dependencies:
```bash
pip install -r requirements-test.txt
```

2. Ensure the application is running or the test client is properly configured.

### Running All Tests

```bash
pytest
```

### Running Specific Test Categories

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests  
pytest -m integration

# Run tests for specific endpoint
pytest tests/test_categories_endpoint.py

# Run tests with coverage
pytest --cov=app tests/
```

### Running Tests with Verbose Output

```bash
pytest -v
```

## Test Categories

### Unit Tests
- Individual endpoint functionality
- Mock external API calls
- Input validation
- Error handling

### Integration Tests
- Complete application flow
- End-to-end scenarios
- Performance under load
- Response format consistency

### Requirements Tests
- Verify all README requirements are met
- Test evaluation criteria compliance
- Check bonus feature implementation

## Mock Strategy

The tests use extensive mocking to:
- **Isolate the application** from external dependencies
- **Control test scenarios** by simulating different API responses
- **Test error conditions** that are difficult to reproduce with real APIs
- **Ensure fast, reliable tests** that don't depend on network connectivity

## Error Scenarios Tested

- External API failures (500, 404, 503)
- Network timeouts and connection errors
- Invalid JSON responses
- Missing required fields in responses
- Malicious input (XSS, SQL injection attempts)
- Rate limiting
- Invalid HTTP methods

## Performance Tests

- Multiple concurrent requests
- Response time validation
- Memory usage patterns
- Caching behavior

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- Fast execution (< 30 seconds for full suite)
- No external dependencies
- Clear pass/fail criteria
- Comprehensive coverage reporting

## Test Data

The tests use realistic mock data that matches the Chuck Norris API format:
- Valid categories from the actual API
- Properly formatted joke responses
- Search results with correct structure
- Error responses that match real API behavior

## Contributing

When adding new features or modifying existing endpoints:
1. Add corresponding test cases
2. Ensure all existing tests pass
3. Update this README if test structure changes
4. Maintain test coverage above 90% 