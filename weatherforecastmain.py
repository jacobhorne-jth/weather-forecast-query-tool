from forward_geocode import ForwardGeocodeAPI, ForwardGeocodeFile
from reverse_geocode import ReverseGeocodeAPI, ReverseGeocodeFile
from weather_data import WeatherDataAPI, WeatherDataFile
from weather_query import WeatherQuery
from output import OutputHandler

'''Main functionality that utilizes other classes and modules'''
def main():
    # Initialize default values for latitude and longitude
    latitude = 0.0
    longitude = 0.0
    output = OutputHandler()  # Output handler instance
    location_data = {}

    # Read the first line of input: Expected format -> COMMAND SOURCE_TYPE ADDRESS
    first_line = input().strip()
    command, source_type, address = first_line.split(maxsplit=2)

    # Forward geocoding to get latitude and longitude based on the address
    if source_type == "NOMINATIM":
        forward = ForwardGeocodeAPI(address)
        location_data = forward.get_location()
        
        # Fetch status and URL for attribution
        status = f'{forward.get_response_status()} '
        url = forward.get_url()
        
        # Update status for geocode operation
        output.status_update(1)
        
    elif source_type == "FILE":
        forward = ForwardGeocodeFile(address)
        location_data = forward.get_location()
        
        status = ''
        url = address  # File path as URL equivalent

    # Extract latitude and longitude from the geocoded location data
    if location_data:
        try:
            display_name = location_data[0]['display_name']
            latitude, longitude = float(location_data[0]['lat']), float(location_data[0]['lon'])
        except Exception as e:
            # Handle incorrect data format or missing fields
            print('FAILED')
            print(f'{status}{url}')
            print('FORMAT')
            return    
    else:
        return
    
    weather_data = {}

    # Read the second line of input: Expected format -> WEATHER SOURCE_TYPE [FILE_NAME]
    second_line = input().strip()
    weather_parts = second_line.split()
    weather_source_type = weather_parts[1]

    # Fetch weather data based on the provided source type (API or file)
    if weather_source_type == "NWS":
        weather = WeatherDataAPI(latitude, longitude)
        weather_data = weather.get_forecast()
        
        # Update status for weather data fetch operation
        output.status_update(3)
        status = f'{weather.get_response_status()} '
        url = weather.get_url()
    elif weather_source_type == "FILE":
        weather_file = weather_parts[2]
        weather_data = WeatherDataFile(weather_file).get_forecast()
        status = ''
        url = weather_file

    # Parse and store weather data if available
    if weather_data:
        try:
            for i in range(len(weather_data['properties']['periods'])):
                coordinate_list = weather_data['geometry']['coordinates']
                temp = weather_data['properties']['periods'][i]['temperature']
                humidity = weather_data['properties']['periods'][i]['relativeHumidity']['value']
                wind = weather_data['properties']['periods'][i]['windSpeed']
                precipitation = weather_data['properties']['periods'][i]['probabilityOfPrecipitation']['value']
                temp_val = weather_data['properties']['periods'][i]['temperatureUnit']
                start = weather_data['properties']['periods'][i]['startTime']
        except Exception as e:
            # Handle incorrect weather data format
            print('FAILED')
            print(f'{status}{url}')
            print('FORMAT')
            return
    else:
        return

    # Process multiple weather queries from user input until 'NO MORE QUERIES' is entered
    while True:
        third_line = input().strip()
        
        if third_line == 'NO MORE QUERIES':
            break

        query_parts = third_line.split()
        query_type = query_parts[0]
        query = WeatherQuery()

        # Handle different types of weather queries (temperature, humidity, wind, precipitation)
        if query_type == 'TEMPERATURE':
            temp_type, temp_scale, temp_length, temp_limit = query_parts[1], query_parts[2], int(query_parts[3]), query_parts[4]
            temp = query.get_temp(weather_data, temp_type, temp_scale, temp_length, temp_limit)
            output.add(temp)
        else:
            temp_length, temp_limit = int(query_parts[1]), query_parts[2]

            if query_type == 'HUMIDITY':
                humidity = query.get_humidity(weather_data, temp_length, temp_limit)
                output.add(humidity)
            elif query_type == 'WIND':
                wind = query.get_wind(weather_data, temp_length, temp_limit)
                output.add(wind)
            elif query_type == 'PRECIPITATION':
                precipitation = query.get_precipitation(weather_data, temp_length, temp_limit)
                output.add(precipitation)

    # Read the fourth line of input for reverse geocoding: Expected format -> REVERSE SOURCE_TYPE [FILE_NAME]
    fourth_line = input().strip().split()
    reverse_source = fourth_line[1]

    # Get the new latitude and longitude from the output handler
    new_lat = output.get_lat_lon(weather_data)[0]
    new_lon = output.get_lat_lon(weather_data)[1]
    
    # Perform reverse geocoding to get location details based on coordinates
    if reverse_source == "NOMINATIM":
        reverse_geocode = ReverseGeocodeAPI(new_lat, new_lon)
        reverse_data = reverse_geocode.get_reverse_data()
        output.print_target(latitude, longitude)
        output.print_forecast(weather_data)
        
        # Fetch status and URL for reverse geocode attribution
        status = f'{reverse_geocode.get_response_status()} '
        url = reverse_geocode.get_url()
        
        # Print the reverse geocoded location name
        print(reverse_geocode.get_reverse_data()['display_name'])
        output.status_update(2)
        
    elif reverse_source == "FILE":
        reverse_file = fourth_line[2]
        reverse_geocode = ReverseGeocodeFile(reverse_file)
        reverse_data = reverse_geocode.get_reverse_data()
        output.print_target(latitude, longitude)
        output.print_forecast(weather_data)
        
        # Print the reverse geocoded location name from file
        print(reverse_geocode.get_reverse_data()['display_name'])
        status = ''
        url = reverse_file

    # Display reverse geocode data if available
    if reverse_data:
        try:
            name = reverse_data['display_name']
        except Exception as e:
            print('FAILED')
            print(f'{status}{url}')
            print('FORMAT')
            return
    else:
        return

    # Final output: print all stored queries and attributions
    output.print_all_queries()
    output.print_attributions()
    

# Entry point of the program
if __name__ == '__main__':
    main()
