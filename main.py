import network
import urequests
import machine
import time

# OpenWeather API s ettings
API_KEY = 'c6ef41a35c89a978157c63adcf0799ab'
LOCATION = 'Ho%20Chi%20Minh'
URL = f"http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}"

# Wi-Fi settings
SSID = 'Pixel_6536'
PASSWORD = 'khanghoang'

SPEED = 1023 #max speed

# Fan PWM settings
FANS = {
    "fan1": machine.PWM(machine.Pin(13), freq=1000),  # Example: Pin 15 for Fan 1
    "fan2": machine.PWM(machine.Pin(5), freq=1000),  # Example: Pin 16 for Fan 2
    "fan3": machine.PWM(machine.Pin(23), freq=1000),  # Example: Pin 17 for Fan 3
    "fan4": machine.PWM(machine.Pin(33), freq=1000),  # Example: Pin 18 for Fan 4
}

# Reference table for fan states
FAN_STATES = {
    "North":      [SPEED, 0, 0, 0],
    "South":      [SPEED, 0, 0, 0],
    "East":       [SPEED, 0, 0, 0],
    "West":       [SPEED, SPEED, SPEED, SPEED],
    "North East": [0, SPEED, 0, 0],
    "North West": [0, SPEED, SPEED, SPEED],
    "South East": [0, SPEED, 0, 0],
    "South West": [SPEED, SPEED, 0, 0],
}

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("Wi-Fi Connected:", wlan.ifconfig())

def get_wind_direction():
    try:
        response = urequests.get(URL)
        weather_data = response.json()
        wind_deg = weather_data["wind"]["deg"]
        response.close()
        
        # Map wind degrees to cardinal directions
        if 0 <= wind_deg < 45 or 315 <= wind_deg <= 360:
            return "North"
        elif 45 <= wind_deg < 135:
            return "East"
        elif 135 <= wind_deg < 225:
            return "South"
        elif 225 <= wind_deg < 315:
            return "West"
        elif 45 <= wind_deg < 90:
            return "North East"
        elif 315 <= wind_deg < 360:
            return "North West"
        elif 135 <= wind_deg < 180:
            return "South East"
        elif 225 <= wind_deg < 270:
            return "South West"
    except Exception as e:
        print("Error fetching wind data:", e)
        return None
    
def control_fans(wind_direction):
    if wind_direction in FAN_STATES:
        states = FAN_STATES[wind_direction]
        for i, (fan_name, fan) in enumerate(FANS.items()):
            fan.duty(states[i])  # Set the PWM duty cycle for each fan
            if states[i] > 0:
                print(f"{fan_name} is turning ON with speed {states[i]}")
            else:
                print(f"{fan_name} is OFF")
    else:
        print("Unknown wind direction. Turning off all fans.")
        for fan_name, fan in FANS.items():
            fan.duty(0)  # Turn off all fans
            print(f"{fan_name} is OFF")

def test():
    print("Testing all fans for 5 seconds...")
    for fan_name, fan in FANS.items():
        fan.duty(1023)  # Turn all fans to full speed
        print(f"{fan_name} is ON at full speed")
    time.sleep(5)  # Wait for 5 seconds
    for fan_name, fan in FANS.items():
        fan.duty(0)  # Turn off all fans
        print(f"{fan_name} is OFF after test")
        
def main():
    test()
    connect_wifi()
    while True:
        wind_direction = get_wind_direction()
        if wind_direction:
            print("Wind Direction:", wind_direction)
            control_fans(wind_direction)
        else:
            print("Failed to fetch wind direction.")
        time.sleep(10)  # Update every 10 seconds

if __name__ == "__main__":
    main()

