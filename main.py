from fastapi import FastAPI, HTTPException, Query, status
import requests
import time
from dotenv import load_dotenv
import os
import json
import logging


# Load environment variables
load_dotenv()

app = FastAPI()

# Cache to store weather API responses temporarily
cache = {}

# Get API key from environment variables
API_KEY = os.getenv("WEATHER_API_KEY")

# If the API key is not set, raise an exception
if not API_KEY:
    raise Exception("Environment variable WEATHER_API_KEY not set")

# Configure logging for debugging purposes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


@app.get("/")
async def home():
    return {"message": "Welcome to the Weather API!"}


@app.get("/weather", status_code=status.HTTP_200_OK)
async def get_weather(city: str = Query(..., description="Enter city name to fetch weather data")):
    # Check if the city is in the cache
    if city in cache:
        time_since_cached = time.time() - cache[city]['timestamp']
        logging.info(f"Cache exists for {city}. Time since cached: {time_since_cached} seconds.")

        if time_since_cached < 12 * 60 * 60:  # Check if cache is less than 12 hours old
            logging.info(f"Using cached data for {city}.")
            return {"source": "cache", "data": cache[city]['data']}
        else:
            logging.info(f"Cache expired for {city}. Fetching new data.")

    # If cache is empty or expired, fetch new data from the API
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={API_KEY}"
    response = requests.get(url)

    # Check for errors in the API response
    if response.status_code != 200:
        logging.error(f"Error fetching data from API for {city}. Status code: {response.status_code}")
        raise HTTPException(
            status_code=response.status_code,
            detail="Error occurred while fetching data from the sweather API"
        )

    # Parse the response JSON
    weather_info = response.json()

    # Save the fetched data in the cache
    cache[city] = {
        "timestamp": time.time(),
        "data": weather_info,
    }
    logging.info(f"Cached new data for {city} with timestamp {cache[city]['timestamp']}.")

    # Save the weather data to a JSON file for persistence
    with open("weather_info.json", 'w') as file:
        json.dump(weather_info, file, indent=4)

    return {"source": "weather api", "data": weather_info, "message": "Weather data fetched and saved successfully."}
