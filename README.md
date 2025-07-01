# weather-forecast-query-tool
A weather forecast tool allowing the user to query real-time weather data using live API calls.

**Overview**

This Python project is a command-line tool that retrieves and processes weather forecast data for a specified location. It integrates geocoding and weather APIs to answer custom weather-related queries such as maximum temperature, minimum humidity, or wind speed over a configurable time horizon.

The project demonstrates how to:

- Programmatically interact with public web APIs, including Nominatim (OpenStreetMap) and the U.S. National Weather Service.

- Perform forward and reverse geocoding to map between place names and coordinates.

- Process JSON data and compute derived weather metrics (e.g., “feels like” temperatures).

- Use object-oriented design with multiple classes encapsulating data sources and query logic.

- Gracefully handle failures due to API errors or unavailable data sources.

**Features**

- Forward Geocoding

    Convert a human-readable place (e.g., Bren Hall, Irvine, CA) into geographic coordinates using Nominatim.

- Reverse Geocoding

    Translate a forecast location’s coordinates back into a descriptive address.

- Hourly Forecast Retrieval

    Fetch hourly weather forecasts from the National Weather Service for a given location.

- Custom Weather Queries

    Support multiple query types:

    - Air temperature (in °F or °C)

    - “Feels like” temperature (heat index or wind chill)

    - Relative humidity

    - Wind speed

    - Chance of precipitation

- Temperature Conversion

    Convert between Fahrenheit and Celsius as requested.

- Fallback Testing with Local Files

    Optionally load saved JSON responses to test without live API calls.

- Failure Reporting

    Detect and report:
  
    - HTTP errors (non-200 status codes)

    - Missing or malformed input files

    - Network connectivity issues

- Attribution Compliance

    Display attribution messages for data sources used during program execution.

**How to Run**

_Prerequisites_
- Python 3.6+

- Internet connection (for live API calls)

- Note: This project intentionally uses only Python’s standard library (e.g., urllib, json)—no third-party packages are required.

<br>

_Running the Program_

Run the main script:

python3 weatherforecastmain.py

- The program expects input lines describing:

- Target location source (Nominatim API or local file)

- Weather data source (National Weather Service API or local file)

- One or more weather queries

- Reverse geocoding source

- Sentinel line indicating end of queries

<br>

Here is an example of an input sequence (typed interactively or piped in):

TARGET NOMINATIM Bren Hall, Irvine, CA

WEATHER NWS

TEMPERATURE AIR F 12 MAX

HUMIDITY 24 MIN

NO MORE QUERIES

REVERSE NOMINATIM

_Press Enter after each line._    

<br>

You can pipe input from a file:

python3 weatherforecastmain.py < example_input.txt    

<br>

Or enter lines interactively as shown above.    

<br>

Example Output

TARGET 33.64324045/N 117.84185686276017/W

FORECAST 33.654532225/N 117.83296842499999/W

1 Sunnyhill, Irvine, CA

2024-11-07T23:00:00Z 77.0000

2024-11-07T22:00:00Z 6.0000%

**Forward geocoding data from OpenStreetMap

**Reverse geocoding data from OpenStreetMap

**Real-time weather data from National Weather Service, United States Department of Commerce    



In case of errors (e.g., network issues or API failure), a clear FAILED report is printed describing the problem.    



_Attribution
_
When live APIs are used, the program will print attribution messages:

OpenStreetMap / Nominatim (for geocoding)

National Weather Service (for weather forecasts)    

<br>

**Project Structure**

weatherforecastmain.py             # Main entry point

forward_geocode.py      # Classes for forward geocoding

reverse_geocode.py      # Classes for reverse geocoding

weather_data.py         # Classes for fetching weather forecasts

weather_query.py        # Classes for computing query results

output.py               # Output formatting and reporting    

<br>

**Notes**
- API Rate Limits: Nominatim requires a 1-second pause between requests. The program enforces this automatically.

- User-Agent and Referer Headers: Required headers are set to comply with API terms of service.

- File Testing: Use local JSON files for testing without relying on live API responses.

- No Third-Party Libraries: All functionality is implemented using the Python standard library.

License
This project is intended for educational use.
