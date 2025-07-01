from datetime import datetime, timezone
class WeatherQuery:
    def convert_time(self, current_time, val):
        """Convert the time to UTC format and append a value."""
        utc_dt = datetime.fromisoformat(current_time).astimezone(timezone.utc)
        return f"{utc_dt.isoformat().replace('+00:00', 'Z')} {val:.4f}"
    
    def find_extreme(self, weather_data, length, key, limit):
        """Find the max or min value for the given key."""
        periods = weather_data['properties']['periods']
        extreme_period = periods[0]
        
        # Handle different structures of weather data
        extreme_value = self.extract_value(periods[0], key)
        counter = int(length)
        
        if len(periods) < counter:
            counter = len(periods)
        
        for i in range(1, counter):
            current_value = self.extract_value(periods[i], key)
            if (limit == 'MAX' and current_value > extreme_value) or (limit == 'MIN' and current_value < extreme_value):
                extreme_value = current_value
                extreme_period = periods[i]
        
        return extreme_period['startTime'], round(extreme_value, 4)

    def extract_value(self, period, key):
        """Extract value from the period dictionary."""
        value = period.get(key)
        # If value is a dictionary (e.g., {'value': 75}), extract the actual value
        if isinstance(value, dict):
            return float(value.get('value', 0))
        # If value is a string like '5 mph', split and convert to int
        elif isinstance(value, str) and key == 'windSpeed':
            return int(value.split()[0])
        return float(value) if value is not None else 0

    def get_temp(self, weather_data, form, scale, length, limit):
        """Get the max or min temperature, either 'AIR' or 'FEELS' like temperature."""
        periods = weather_data['properties']['periods']
        temperatureUnit = weather_data['properties']['periods'][0]['temperatureUnit']
        temperature_list = []
        counter = int(length)
        
        if len(periods) < counter:
            counter = len(periods)
            
        for i in range(counter):
            T = float(periods[i]['temperature'])
            unit = periods[i]['temperatureUnit']
            if form == 'FEELS':
                H = float(periods[i]['relativeHumidity']['value'])
                W = float(periods[i]['windSpeed'].split(' ')[0])
                T = self.calculate_feels_like_temp(T, H, W)
            if unit == 'C':
                T = T * 9 / 5 + 32
            temperature_list.append((periods[i]['startTime'], T))

        # Find max or min temperature
        extreme_time, extreme_temp = temperature_list[0]
        for time, temp in temperature_list:
            if (limit == 'MAX' and temp > extreme_temp) or (limit == 'MIN' and temp < extreme_temp):
                extreme_temp = temp
                extreme_time = time

        if scale == 'C':
            extreme_temp = (extreme_temp - 32) * 5 / 9  # Convert to Celsius

        return self.convert_time(extreme_time, round(extreme_temp, 4))

    def get_humidity(self, weather_data, length, limit):
        """Get the max or min humidity."""
        hour, humidity = self.find_extreme(weather_data, length, 'relativeHumidity', limit)
        return f"{self.convert_time(hour, humidity)}%"

    def get_wind(self, weather_data, length, limit):
        """Get the max or min wind speed."""
        hour, wind_speed = self.find_extreme(weather_data, length, 'windSpeed', limit)
        return self.convert_time(hour, wind_speed)

    def get_precipitation(self, weather_data, length, limit):
        """Get the max or min probability of precipitation."""
        hour, precipitation = self.find_extreme(weather_data, length, 'probabilityOfPrecipitation', limit)
        return self.convert_time(hour, round(precipitation, 4))

    def calculate_feels_like_temp(self, T, H, W):
        """Calculate the 'feels like' temperature using heat index or wind chill formula."""
        if T >= 68.0:  # Heat Index
            return (-42.379 + 2.04901523 * T + 10.14333127 * H - 0.22475541 * T * H
                    - 0.00683783 * T**2 - 0.05481717 * H**2 + 0.00122874 * T**2 * H
                    + 0.00085282 * T * H**2 - 0.00000199 * T**2 * H**2)
        elif T <= 50.0 and W > 3.0:  # Wind Chill
            return 35.74 + 0.6215 * T - 35.75 * W**0.16 + 0.4275 * T * W**0.16
        return T
