import json
import urllib.request

"""Class for NWS API Usage"""
class WeatherDataAPI:
    def __init__(self, latitude, longitude):
        """initializes weather api objects"""
        self.latitude = latitude
        self.longitude = longitude
        self.current_status = ''
        self.full_url = ''

    def get_response_status(self) -> int:
        """get current status to check for errors"""
        return self.current_status

    def get_url(self) -> str:
        """get url to check for errors"""
        return self.full_url

    def get_forecast(self) -> dict:
        """requests response and gets forecase"""
        self.full_url = f"https://api.weather.gov/points/{self.latitude},{self.longitude}"
        request = urllib.request.Request(self.full_url, headers={"User-Agent": "(https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/, jhorne1@uci.edu)"})
    
        try:
            with urllib.request.urlopen(request) as response:
                self.current_status = response.status
                if response.status != 200:
                    print('FAILED')
                    print(f'{response.status} {self.full_url}')
                    print('NOT 200')
                    return {}
                data = json.load(response)
                forecast_url = data['properties']['forecastHourly']
                forecast_request = urllib.request.Request(forecast_url, headers={
                    "Accept": "application/geo+json",
                    "User-Agent": "(https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/, jhorne1@uci.edu)"})

                with urllib.request.urlopen(forecast_request) as forecast_response:
                    self.current_status = response.status
                    if response.status != 200:
                        print('FAILED')
                        print(f'{response.status} {self.full_url}')
                        print('NOT 200')
                        return {}
                    return json.load(forecast_response)
        except (urllib.error.HTTPError, OSError):
            print('FAILED')
            print(f'{self.current_status}{self.full_url}')
            print('NETWORK')
            return {}
        except Exception as e:
            print('FAILED')
            print(f'{self.current_status}{self.full_url}')
            print('FORMAT')
            return {}

"""class for weather file data usage"""
class WeatherDataFile:
    """initializes file objects"""
    def __init__(self, file_path):
        self.file_path = file_path
        
    """gets forecase based on file"""
    def get_forecast(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError, IOError):
            print('FAILED')
            print(f'{self.file_path}')
            print('MISSING')
            return {}
