import json
import urllib.parse
import urllib.request

"""Class for reverse geocode api"""
class ReverseGeocodeAPI:
    """initializes reverse geocode api objects"""
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.current_status = ''
        self.full_url = ''

    """gets current response"""
    def get_response_status(self) -> int:
        return self.current_status
    
    """gets current url"""
    def get_url(self) -> str:
        return self.full_url

    """gets reverse data and checks for errors"""
    def get_reverse_data(self):
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {"lat": self.latitude, "lon": self.longitude, "format": "jsonv2"}
        self.full_url = f"{url}?{urllib.parse.urlencode(params)}"
        request = urllib.request.Request(self.full_url, headers={"Referer": "https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/jhorne1"})

        try:
            with urllib.request.urlopen(request) as response:
                self.current_status = response.status
                if response.status != 200:
                    print('FAILED')
                    print(f'{response.status} {full_url}')
                    print('NOT 200')
                    return {}
                return json.loads(response.read().decode())
        except (urllib.error.HTTPError, OSError):
            print('FAILED')
            print(f'{self.current_status} {self.full_url}')
            print('NETWORK') 
        except Exception as e:
            print('FAILED')
            print(f'{self.current_status} {self.full_url}')
            print('FORMAT')
            return {}
"""Class for reverse code with files"""
class ReverseGeocodeFile:
    """initializes file objects"""
    def __init__(self, file_path):
        self.file_path = file_path

    """gets reverse geocode data from file"""
    def get_reverse_data(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return data
        except (FileNotFoundError, json.JSONDecodeError, IOError):
            print('FAILED')
            print(f'{self.file_path}')
            print('MISSING')
            return {}
