
### README - WEATHER API 

## pip install fastapi uvicorn requests python-dotenv

FastAPI: For building the API.

requests: A library to make HTTP requests to external APIs.

time: Used to manage timestamps for caching.

Optional: From Python's typing module, used for type hinting (not directly used in 
this code).

Uvicorn: For running the FastAPI app.

Requests: For making HTTP requests to the 3rd party API.

python-dotenv: For managing environment variables.


# Define the Weather Endpoint

The function takes a city query parameter:
city: The name of the city for which weather data is fetched.
Query(...): Validates the parameter, marking it as required and providing a description.

# Fetch Data from the Weather API
If the cache is empty or expired, the function builds a URL to fetch weather data from the Visual Crossing Weather API:

requests.get(url): Makes a GET request to the API and stores the response.


If the response from the API has an error (status code not 200), the function raises an HTTPException with the appropriate status code and error message.


The weather information is parsed from the API response, assuming it is in JSON format.





The expression 12 * 60 * 60 calculates the number of seconds in 12 hours. Here's how it's broken down:

60 seconds in a minute
60 minutes in an hour
Multiply by 12 to represent 12 hours.

43,200 seconds equals 12 hours.

