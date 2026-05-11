import requests

class Forecast:
    def __init__(self, temperature, windspeed, rain=0):
        self.temperature = temperature
        self.windspeed = windspeed
        self.rain = rain

class WeatherClient:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, lat, lon):
        try: 
            params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }
            response = requests.get(self.base_url,params=params, timeout=10)

            if response.status_code != 200:
                raise Exception("Failed to fetch weather data")
            
            data = response.json()
            weather = data.get("current_weather", {})
            
            return Forecast(
                temperature = weather.get("temperature"),
                windspeed = weather.get("windspeed"),
                rain = weather.get("precipitation, 0")
            )
        except requests.exceptions.RequestException:
            raise Exception("Network error: Check your internet connection")
        except Exception as e:
            raise Exception(f"Error: {e}")
    def get_coordinates(self, location):
        try:
            url = "https://geocoding-api.open-meteo.com/v1/search"
            params = {
                "name": location,
                "count": 1
            }
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                raise Exception("Failed to fetch location data")
            
            data = response.json()
            results = data.get("results")

            if not results:
                raise Exception("Location not found")

            lat = results[0]["latitude"]
            lon = results[0]["longitude"]

            return lat, lon

        except requests.exceptions.RequestException:
            raise Exception("Network error: Check your internet connection")
        except Exception as e:
            raise Exception(f"Error: {e}")
