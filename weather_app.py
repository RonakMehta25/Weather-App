import requests
import sys
from api_keys import api_keys

# Set API key and base URL for OpenWeatherMap API
base_url = 'https://api.openweathermap.org/data/2.5/weather?'

# Get user's current IP address
ip_response = requests.get('https://api.ipify.org?format=json')
ip_data = ip_response.json()
ip_address = ip_data['ip']


# Get user's location (for example, by asking them to input their city)
#city = input('Enter city name: ')


# Use IPGeolocation API to get user's location based on IP address
location_url='https://api.ipgeolocation.io/ipgeo?apiKey=' + api_keys["ipgeolocation"] + '&ip=' + ip_address
print(f'location_url={location_url}')
location_response = requests.get(location_url)

location_data = location_response.json()

if 'message' in location_data:
	print(f"Error: {location_data['message']}")
	sys.exit(1)
else:
	# Extract city name from location data
	city = location_data['city']


# Build API query URL
query_url = base_url + 'q=' + city + '&appid=' + api_keys["openweathermap"]

print(f'query_url={query_url}')

# Send GET request to API
response = requests.get(query_url)

# If request was successful (status code 200), parse JSON response and extract weather data
if response.status_code == 200:
    data = response.json()
    temp = data['main']['temp'] - 273.15
    description = data['weather'][0]['description']
    wind_speed = data['wind']['speed']

    # Display weather data to user
    print(f'The current temperature in {city} is {temp:.1f} Celsius.')
    print(f'The weather is {description}.')
    print(f'The wind speed is {wind_speed} meters per second.')
else:
    # If request was not successful, display error message
    print('Error: Could not retrieve weather data.')