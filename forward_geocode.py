import json
import urllib.parse
import urllib.request

"""forward geocode api object class"""
class ForwardGeocodeAPI:
    def __init__(self, address):
        self.address = address
        self.current_status = ''
        self.full_url = ''

    """returns current response"""
    def get_response_status(self) -> int:
        return self.current_status

    """returns url"""
    def get_url(self) -> str:
        return self.full_url

    """gets location using request and forward geocoding and checks for errors"""
    def get_location(self):
        url = 'https://nominatim.openstreetmap.org/search'
        params = {'q': self.address, 'format': 'jsonv2', 'limit': '1'}
        query_string = urllib.parse.urlencode(params)
        self.full_url = f"{url}?{query_string}"
        request = urllib.request.Request(self.full_url, headers={"Referer": "https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/jhorne1"})

        try:
            with urllib.request.urlopen(request) as response:
                self.current_status = response.status
                if response.status != 200:
                    print('FAILED')
                    print(f'{response.status} {self.full_url}')
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

"""forward geocode using files"""
class ForwardGeocodeFile:
    def __init__(self, file_path):
        self.file_path = file_path
        
    """gets location based on file, checks for error"""
    def get_location(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError, IOError):
            print('FAILED')
            print(f'{self.file_path}')
            print('MISSING')
            return {}
