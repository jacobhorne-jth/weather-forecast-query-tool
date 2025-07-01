class OutputHandler: 
    def __init__(self):
        self.outputs = []
        self.forward_status = False
        self.reverse_status = False
        self.weather_status = False

    def add(self, data):
        """Add a new output entry."""
        self.outputs.append(data)

    def print_all_queries(self):
        """Print all stored outputs."""
        for output in self.outputs:
            print(output)

    def calculate_coords(self, latitude, longitude: float) -> str:
        """calculate coords and adjusts S and N and E and W based on the values"""
        lat_direction = 'N' if latitude >= 0 else 'S'
        lon_direction = 'E' if longitude >= 0 else 'W'

        latitude = abs(latitude)
        longitude = abs(longitude)
        
        return f'{latitude}/{lat_direction} {longitude}/{lon_direction}'

    
    def print_target(self, latitude, longitude: float) -> None:
        """print target latitude and longitude"""
        coords = self.calculate_coords(latitude, longitude)
        print(f'TARGET {coords}')
        

    def get_lat_lon(self, weather_data: dict) -> list:
        """calculate latitude and longitude based on polygon of points"""
        outputs = list()
        coordinates = weather_data['geometry']['coordinates'][0]
        unique_points = set()  # Use a set to store unique points
        latitudes = list()
        longitudes = list()
    
        for point in coordinates:
            unique_points.add(tuple(point)) 
    
        for point in unique_points:
            latitudes.append(point[1])
            longitudes.append(point[0])
        
        outputs.append(sum(latitudes) / len(latitudes) if latitudes else 0)
        outputs.append(sum(longitudes) / len(longitudes) if longitudes else 0)
        
        return outputs

    def print_forecast(self, weather_data: dict) -> None:
        """print forecast and latitude and longitude values"""
        avg_longitude = self.get_lat_lon(weather_data)[1]
        avg_latitude = self.get_lat_lon(weather_data)[0]
        
        coords = self.calculate_coords(avg_latitude, avg_longitude)

        print(f'FORECAST {coords}')


    def status_update(self, num: int) -> None:
        """updates status for the attributions"""
        if num == 1:
            self.forward_status = True
        elif num == 2:
            self.reverse_status = True
        else:
            self.weather_status = True

    def print_attributions(self) -> None:
        """prints attributions"""
        if self.forward_status:
            print('**Forward geocoding data from OpenStreetMap')
        if self.reverse_status:
            print('**Reverse geocoding data from OpenStreetMap')
        if self.weather_status:
            print('**Real-time weather data from National Weather Service, United States Department of Commerce')
