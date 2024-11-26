import machine
import neopixel
import time
import random

# Configuration
from effects import effect_config  # Import the configuration file
# Load the number of LEDs from the config file
num_leds = effect_config.NUM_LEDS
pin = 10  # GPIO pin connected to the NeoPixel data input

# Initialize NeoPixel
np = neopixel.NeoPixel(machine.Pin(pin), num_leds)

# Base dimming color values for purple
base_r = 7  # Base red value (dimmed)
base_g = 3   # Base green value (dimmed)
base_b = 15  # Base blue value (dimmed)

# Adjusted yellow color values (less green, more blue)
yellow_r = 255  # Red value for yellow
yellow_g = 130  # Green value for yellow (reduced)
yellow_b = 5  # Blue value for yellow (increased)

__all__ = ['play_effect'] 


def set_all_color(color):
    for i in range(num_leds):
        np[i] = color
    np.write()

def get_random_adjacent_leds(count):
    # Get a random starting index for 'count' adjacent LEDs
    start_index = random.randint(0, num_leds - count)
    return list(range(start_index, start_index + count))

def random_leds_up_down(selected_leds):
    # Set LEDs to adjusted yellow and gradually change brightness
    for brightness in range(0, 256, 5):  # Increase brightness
        for led in selected_leds:
            np[led] = (int(brightness * yellow_r / 255), 
                       int(brightness * yellow_g / 255), 
                       int(brightness * yellow_b / 255))  # Adjusted yellow color
        np.write()
        time.sleep(0.05)  # Adjust the delay for speed

    for brightness in range(255, -1, -5):  # Decrease brightness
        for led in selected_leds:
            np[led] = (int(brightness * yellow_r / 255), 
                       int(brightness * yellow_g / 255), 
                       int(brightness * yellow_b / 255))  # Adjusted yellow color
        np.write()
        time.sleep(0.05)  # Adjust the delay for speed

    # Reset selected LEDs back to base purple color
    for led in selected_leds:
        np[led] = (base_r, base_g, base_b)  # Purple color
    np.write()
    time.sleep(0.1)  # Optional: Delay before the next effect

def play_effect(duration_minutes):
    print("Playing 'clear night' effect")
    start_time = time.time()  # Record the start time
    duration_seconds = duration_minutes * 60  # Convert minutes to seconds

    # Start with all LEDs in purple
    set_all_color((base_r, base_g, base_b))  # Purple color
    time.sleep(1)

    while True:
        # Select 4 sets of adjacent random LEDs
        selected_leds_sets = []
        
        for _ in range(4):  # Create 4 sets
            while True:
                new_set = get_random_adjacent_leds(3)
                # Ensure the new set does not overlap with already selected sets
                if all(not (set_ == new_set or set(new_set).intersection(set(set_))) for set_ in selected_leds_sets):
                    selected_leds_sets.append(new_set)
                    break

        # Run the pulsing effect on each selected set
        for selected_leds in selected_leds_sets:
            random_leds_up_down(selected_leds)

        time.sleep(0.5)  # Delay before selecting new LEDs

        # Check if the duration has been reached
        if time.time() - start_time >= duration_seconds:
            break  # Exit the loop after the duration

    

