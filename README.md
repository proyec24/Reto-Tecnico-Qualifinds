# Jr Backend Engineer Code Challenge

- **Estimated time:** 20 minutes
- **Difficulty:** Junior
- **Suggested stack:** Any (NodeJS, Python, Ruby, Go, etc.)

### Your goal:

Build a backend application that
exposes the endpoints described below, consumes data from the specified public APIs and returns the responses also described below.

#### Context: 
The Chuck Norris API lets you retrieve random jokes, category-specific jokes, search for jokes
by keyword, and even personalize jokes with usernames. The original app even predates Slack!
But for this challenge, we'll focus only on two endpoints.

### Requirements

1. GET `/categories`

Returns a list of the available joke categories.

Internally calls:
https://api.chucknorris.io/jokes/categories

Expected response:

`
[
    "A", 
    "List", 
    "Of", 
    "Jokes", 
    "Categories"
]
`

2. GET `joke/{category}`

Returns a random joke from the specified category.

Internally calls:
https://api.chucknorris.io/jokes/random?category={category}

Expected response:

`{
    "id" : "requestId",
    "url" : "publicApiUrl",
    "value" : "The joke in string"
}`

#### We expect that you...

* Use clear, clean code.
* Handle edge cases (e.g. invalid category).
* Return meaningful HTTP status codes.
* No need for persistence or authentication.

#### Bonus (Optional)

If you finish early, consider adding:
* A GET /search?query=term endpoint using:
https://api.chucknorris.io/jokes/search?query=term
* Validate that the provided category exists before requesting a joke.
* Input validation & graceful error handling.
* A README file with setup/run instructions.

#### Evaluation Criteria
* Functional correctness.
* Code clarity and structure.
* Error handling and edge case coverage.
* Ability to consume and transform external APIs.
* Code reusability and modularity (if applicable).

## 🚀 Automated Testing & Timing

This challenge includes an automated testing system that measures completion time and evaluates your implementation.

### Quick Start (GitHub Codespaces)

1. **Open in Codespace**: Click "Code" → "Open with Codespaces"
2. **Start Timer**: `python challenge_timer.py start`
3. **Implement Endpoints**: Build your API
4. **Test Progress**: `python challenge_timer.py test`
5. **Complete Challenge**: `python challenge_timer.py stop`

### Local Development

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Start the challenge timer
python challenge_timer.py start

# Test your progress
python challenge_timer.py test

# Run full test suite
python challenge_timer.py full

# Stop timer and get report
python challenge_timer.py stop
```

### What Gets Measured

#### ⏱️ Completion Time
- **Start Time**: When you begin the challenge
- **End Time**: When you complete minimal requirements
- **Duration**: Total time in seconds and minutes

#### 🧪 Test Results
- **Minimal Tests**: Required endpoints (GET /categories, GET /joke/{category})
- **Full Tests**: Bonus features and edge cases
- **Coverage**: Code coverage and quality metrics

#### 📊 Performance Evaluation
- 🚀 **EXCELLENT** - < 10 minutes
- ✅ **GOOD** - 10-20 minutes  
- ⚠️ **SLOW** - 20-30 minutes
- 🐌 **VERY SLOW** - > 30 minutes

### GitHub Actions Integration

The system automatically runs tests on push/PR and provides:
- ⏱️ Completion time measurement
- 🧪 Automated test execution
- 📊 Coverage reports
- 💬 PR comments with results
- 📦 Test artifacts

### Interactive Mode

```bash
python challenge_timer.py
```

Commands:
- `start` - Start the challenge timer
- `test` - Run minimal required tests
- `full` - Run complete test suite
- `stop` - Stop timer and generate report
- `report` - Generate completion report
- `quit` - Exit the program

## 📋 Challenge Requirements Summary

### Required Endpoints
1. **GET /categories** - Returns list of joke categories
2. **GET /joke/{category}** - Returns random joke with `id`, `url`, `value`

### Bonus Features (Optional)
- **GET /search?query=term** - Search functionality
- **Category Validation** - Validate categories before requests
- **Input Validation** - XSS and injection prevention
- **Graceful Error Handling** - Network and API failures

## 📊 Sample Output

### Timer Start
```
🎯 Chuck Norris API Challenge Started!
⏱️  Timer is now running...
📋 Complete the required endpoints:
   - GET /categories
   - GET /joke/{category}
```

### Progress Test
```
🧪 Running minimal required tests...
📋 Categories endpoint: ✅ PASSED
📋 Joke endpoint: ✅ PASSED
🎉 CONGRATULATIONS! You've completed the minimal requirements!
```

### Completion Report
```
============================================================
🎯 CHALLENGE COMPLETION REPORT
============================================================
⏱️  Total Time: 847.3 seconds (14.1 minutes)
📅 Started: 2024-01-15T10:30:00
📅 Finished: 2024-01-15T10:44:07
📊 Performance: ✅ GOOD - Reasonable completion time
============================================================
```

## 🔧 Development Environment

### GitHub Codespaces
- Pre-configured Python 3.11 environment
- VS Code extensions for Python development
- Automatic dependency installation
- Port forwarding for web applications

### Local Setup
```bash
# Install dependencies
pip install -r requirements-test.txt

# Run tests
python run_tests.py

# Run with coverage
python run_tests.py --coverage
```

## 📁 Project Structure

```
backend-challenge-jr/
├── README.md                    # This file
├── challenge_timer.py           # Timer and test runner
├── run_tests.py                 # Test execution script
├── requirements-test.txt        # Test dependencies
├── tests/                       # Test suite
│   ├── test_categories_endpoint.py
│   ├── test_joke_endpoint.py
│   ├── test_bonus_endpoints.py
│   ├── test_integration.py
│   ├── test_requirements.py
│   └── README.md
├── .github/
│   ├── workflows/
│   │   └── test-challenge.yml  # GitHub Actions workflow
│   └── codespaces/
│       └── devcontainer.json   # Codespace configuration
├── automated_testing.md         # Detailed testing documentation
└── TEST_SUMMARY.md             # Test coverage summary
```

## 🎯 Evaluation

Your implementation will be evaluated on:

1. **Functional Correctness** - Do the endpoints work correctly?
2. **Code Quality** - Is the code clean and well-structured?
3. **Error Handling** - Are edge cases handled properly?
4. **Speed** - How quickly did you complete the challenge?
5. **Bonus Features** - Did you implement optional features?

The automated testing system provides objective metrics for all these criteria.

## 📚 Additional Resources

- [Automated Testing Documentation](automated_testing.md) - Detailed testing guide
- [Test Summary](TEST_SUMMARY.md) - Complete test coverage analysis
- [Test Suite README](tests/README.md) - Test suite documentation

Good luck with the challenge! 🚀