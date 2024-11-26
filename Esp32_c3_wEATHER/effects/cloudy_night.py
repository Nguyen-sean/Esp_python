import machine
import neopixel
import time
import math
from effects import effect_config  # Import the configuration file

# Load the number of LEDs from the config file
num_leds = effect_config.NUM_LEDS
# Pin where the NeoPixel data line is connected
pin = 10  # Use GPIO10 or another available GPIO pin

# Initialize NeoPixel object
np = neopixel.NeoPixel(machine.Pin(pin), num_leds)

# Base dimming color values for purple
base_r = 30  # Base red value (dimmed)
base_g = 5  # Base green value (dimmed)
base_b = 35  # Base blue value (dimmed)

__all__ = ['play_effect'] 


# Function to create a wavy cloudy effect using sine wave
def play_effect(duration_minutes):
    print("Playing 'cloudy night' effect")
    start_time = time.time()  # Record the start time
    duration_seconds = duration_minutes * 60  # Convert minutes to seconds

    while True:  # Infinite loop to keep the effect running
        for i in range(num_leds):
            # Set base color for each LED
            np[i] = (base_r, base_g, base_b)

            # Create a slower sine wave effect for brightness
            wave_position = (i + time.ticks_ms() / 700) % (2 * math.pi)  # Adjust divisor for slower movement
            brightness_factor = (math.sin(wave_position) + 1) / 2  # Normalize to range [0, 1]

            # Calculate final color values for the wave effect
            wave_r = min(255, base_r + int(7 * brightness_factor)*15)  # Adjust wave intensity
            wave_g = min(255, base_g + int(7 * brightness_factor)*4)
            wave_b = min(255, base_b + int(00 * brightness_factor))

            # Apply the updated color to the LED
            np[i] = (wave_r, wave_g, wave_b)

        np.write()  # Update the LED strip with the new colors

        time.sleep(0.14)  # Longer delay for smoother movement

        # Check if the duration has been reached
        if time.time() - start_time >= duration_seconds:
            break  # Exit the loop after the duration