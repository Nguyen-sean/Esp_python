import urequests
import time
from effects import standby
from data_config import OPENWEATHER_API_KEY, LOCATION

def get_weather(api_key = OPENWEATHER_API_KEY, location= LOCATION, delay=1):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    print("Fetching weather for", location)
    
    while True:  # Keep trying indefinitely until successful
        try:
            response = urequests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_id = data['weather'][0]['id']
                return categorize_weather(weather_id)
            else:
                print("Error fetching weather data, status code:", response.status_code)
        except Exception as e:
            print(f"Error occurred with weather: {e}")
        
        print("Retrying in", 1, "seconds...")
        standby(0.6)
        time.sleep(0.1)
        
def categorize_weather(weather_id):
    # Get the current time in hours
    current_time = time.localtime()  # Get the current local time
    hour = current_time[3]  # Extract the hour from the tuple (index 3)

    # Grouping weather conditions
    if 200 <= weather_id < 300:
        return "stormy"  # Thunderstorms
    elif 300 <= weather_id < 600:
        return "rainy"   # Drizzle, Rain
    elif 600 <= weather_id < 700:
        return "snowy"   # Snow
    elif 700 <= weather_id < 800:
        return "foggy"   # Atmosphere
    elif weather_id == 800:
        # Check if it's day or night
        if 6 <= hour < 18:
            return "sunny"  # Daytime (6 AM to 6 PM)
        else:
            return "clear_night"  # Nighttime (6 PM to 6 AM)
    elif 801 <= weather_id < 900:
        if 6 <= hour < 18:
            return "cloudy"   # Clouds
        else:
            return "cloudy_night"  # Nighttime (6 PM to 6 AM)
    
    return "unknown"      # Any other condition

# Example usage
#if __name__ == "__main__":
 #   weather_condition = get_weather()
  #  print("Current weather condition:", weather_condition)