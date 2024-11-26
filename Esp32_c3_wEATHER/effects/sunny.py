import machine
import neopixel
import time

# Configuration
from effects import effect_config  # Import the configuration file
# Load the number of LEDs from the config file
num_leds = effect_config.NUM_LEDS
pin = 10  # GPIO pin connected to the NeoPixel data input

# Initialize NeoPixel object
np = neopixel.NeoPixel(machine.Pin(pin), num_leds)

# Base dimming color values
base_r = 35  # Base red value (dimmed)
base_g = 40  # Base green value (dimmed)
base_b = 60  # Base blue value (dimmed)

__all__ = ['play_effect'] 


# Function to create a subtle glow-up effect with fading edges
def play_effect(duration_minutes):
    print("Playing 'sunny' effect")
    offset = 0  # Initial offset for glow movement
    glow_increase = 20  # Amount to increase brightness for the main glow
    fade_length = 12  # Number of LEDs to fade in and out at the edges
    
    start_time = time.time()  # Record the start time
    duration_seconds = duration_minutes * 60  # Convert minutes to seconds

    while True:  # Infinite loop to keep the effect running
        for i in range(num_leds):
            # Set base color for each LED
            np[i] = (base_r, base_g, base_b)

        # Apply glow-up to around 10 LEDs with fading edges
        for i in range(-fade_length, 10 + fade_length):
            index = (offset + i) % num_leds  # Wrap around if index exceeds the strip length
            
            # Calculate the brightness for fading edges
            if i < 0 or i >= 10:
                # Fading part
                brightness_factor = max(0, 1 - abs(i) / fade_length)
            else:
                # Main glow part
                brightness_factor = 1

            # Calculate final color values for the glow effect with fade
            glow_r = min(255, base_r + int(glow_increase * brightness_factor * 10))
            glow_g = min(255, base_g + int(glow_increase * brightness_factor * 10))
            glow_b = min(255, base_b + int(glow_increase * brightness_factor * 0))

            # Apply the updated color to the LED
            np[index] = (glow_r, glow_g, glow_b)

        np.write()  # Update the LED strip with the new colors

        # Move the glow to the right
        offset += 1
        if offset >= num_leds:
            offset = 0  # Restart the glow from the beginning

        time.sleep(0.095)  # Delay for smooth and slower movement

        # Check if the duration has been reached
        if time.time() - start_time >= duration_seconds:
            break  # Exit the loop after the duration

