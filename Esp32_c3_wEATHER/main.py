import time
import weather
import urequests
from effects import * 
from data_config import THINGSPEAK_API_KEY, THINGSPEAK_ID

# wifi.py
import network
import wifi

interval_time = 10 #time for each efffect playing - 10 minutes

def test_effect():
    sunny(0.15)
    clear_night(0.15)
    stormy(0.15)
    cloudy(0.15)
    cloudy_night(0.15)
    rainy(0.15)

def upload_weather_condition(condition):
    url = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}&field1={condition}"
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            print("Successfully uploaded weather condition to ThingSpeak.")
        else:
            print("Failed to upload weather condition:", response.text)
    except Exception as e:
        print("Error uploading to ThingSpeak:", e)

def main():
    print("starting")
    
    while True:
        station = network.WLAN(network.STA_IF)

        # Check if connected to WiFi
        if not station.isconnected():
            print("reconnecting")
            wifi.connect()

        # Fetch weather data
        weather_condition = weather.get_weather()
        # Upload weather condition to ThingSpeak
        upload_weather_condition(weather_condition)
        
        # Print statement based on weather condition
        if weather_condition == "sunny": sunny(interval_time)  # Play for 10 minutes
        elif weather_condition == "clear_night": clear_night(interval_time)  # Play for 10 minutes
        elif weather_condition == "rainy": rainy(interval_time)   # Play for 10 minutes
        elif weather_condition == "cloudy": cloudy(interval_time)  # Uncomment when cloudy effect is implemented
        elif weather_condition == "cloudy_night": clear_night(interval_time)  # Play for 10 minutes
        elif weather_condition == "stormy": stormy(interval_time)   # Play for 10 minutes
        elif weather_condition == "snowy": print("Playing 'snowy' effect")
        elif weather_condition == "foggy": print("Playing 'foggy' effect")
        else:
            print("Unknown weather condition, no effect to play.")

riseup()
test_effect()
main()

