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