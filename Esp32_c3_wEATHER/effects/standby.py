import machine
import neopixel
import time
import math

# Configuration
from effects import effect_config  # Import the configuration file
# Load the number of LEDs from the config file
num_leds = effect_config.NUM_LEDS
pin = 10  # GPIO pin connected to the NeoPixel data input

# Initialize NeoPixel object
np = neopixel.NeoPixel(machine.Pin(pin), num_leds)

__all__ = ['play_effect'] 


# Function to convert a position in the spectrum to RGB
def spectrum_to_rgb(position):
    # Position is in range [0, 1]
    r = int((1 + math.sin(2 * math.pi * (position + 0.00))) * 127.5)
    g = int((1 + math.sin(2 * math.pi * (position + 0.33))) * 127.5)
    b = int((1 + math.sin(2 * math.pi * (position + 0.66))) * 127.5)
    return r, g, b

# Function to create a waving effect with each LED set to a color on the continuous spectrum
def play_effect(duration_minutes):
    print("Playing 'spectrum wave' effect")
    start_time = time.time()  # Record the start time
    duration_seconds = duration_minutes * 60  # Convert minutes to seconds

    while True:
        current_time = time.ticks_ms() / 6000  # Adjust divisor to control wave speed
        for i in range(num_leds):
            # Calculate the position in the spectrum for each LED
            spectrum_position = (i / num_leds + current_time) % 1  # Wrap around [0, 1]
            r, g, b = spectrum_to_rgb(spectrum_position)

            # Apply the calculated color to the LED
            np[i] = (r, g, b)

        np.write()  # Update the LED strip with the new colors

        time.sleep(0.07)  # Adjust delay for smoother movement

        # Check if the duration has been reached
        if time.time() - start_time >= duration_seconds:
            break  # Exit the loop after the duration

