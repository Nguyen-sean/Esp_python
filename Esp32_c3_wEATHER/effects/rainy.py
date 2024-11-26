import machine
import neopixel
import time
import random

# Configuration
from effects import effect_config  # Import the configuration file
# Load the number of LEDs from the config file
num_leds = effect_config.NUM_LEDS
pin = 10  # GPIO pin connected to the NeoPixel data input

# Initialize NeoPixel object
np = neopixel.NeoPixel(machine.Pin(pin), num_leds)

__all__ = ['play_effect'] 


# Function to reduce green by 15%
def adjust_green(r, g, b):
    return r, int(g * 0.85), b  # Reduce green by 15%

# Function to set all LEDs to a dimmed state with the white color
def set_all_dim():
    base_color = (170, 170, 120)  # White color for the dim state
    dim_factor = 0.1  # Adjust this value for the overall dimmed brightness
    adjusted_color = adjust_green(int(base_color[0] * dim_factor),
                                  int(base_color[1] * dim_factor),
                                  int(base_color[2] * dim_factor))
    
    for i in range(num_leds):
        np[i] = adjusted_color
    np.write()

# Function to gradually change the brightness of a "raindrop" LED
def raindrop_brighten_fade(index, brightness):
    # Calculate color values for raindrop effect, with blue 20% brighter
    blue_brightness = int(min(255, brightness * 2.5))  # Blue is 20% brighter
    red_green_brightness = int(min(255, brightness))  # Red and green are normal

    np[index] = (red_green_brightness, red_green_brightness, blue_brightness)
    np.write()

# Function to simulate lightning effect with 5 adjacent LEDs
def storm_effect():
    print("kachow")
    for _ in range(3):  # Flicker the flash three times
        # Light up all LEDs in bright yellow color
        for i in range(num_leds):
            np[i] = (255, 200, 42)  # Bright yellow color
        np.write()
        
        time.sleep(random.uniform(0.05, 0.1))  # Random delay for flicker duration
        
        # Turn off all LEDs
        for i in range(num_leds):
            np[i] = (0, 0, 0)  # Turn off
        np.write()
        
        time.sleep(random.uniform(0.05, 0.15))  # Random delay between flickers
    
    # Reset to dimmed state
    set_all_dim()  # Reset to dimmed state


# Main loop for the rain effect
def play_effect(duration_minutes):
    print("Playing 'rainy' effect")
    set_all_dim()  # Set all LEDs to a dimmed state
    active_raindrops = {}  # Keep track of fading raindrop LEDs
    start_time = time.time()  # Record the start time
    duration = duration_minutes * 60  # Run for the specified duration

    lightning_timer = time.time()  # Timer for lightning effects
    
    while True:
        # Check if duration has passed
        if time.time() - start_time > duration:
            break
        
        
        # Check for lightning effect every 10 seconds
        if time.time() - lightning_timer >= 20:  # Trigger lightning every 10 seconds
            storm_effect()
            lightning_timer = time.time()  # Reset lightning timer
        
        # Randomly choose LEDs to brighten as "raindrops"
        if random.random() < 0.2:  # Lower chance for new raindrops
            led_index = random.randint(0, num_leds - 1)
            if led_index not in active_raindrops:
                active_raindrops[led_index] = {
                    "brightness": 30,   # Start from dim brightness
                    "direction": 10      # Brighten (increase brightness)
                }

        # Update brightness of active "raindrop" LEDs
        for led_index in list(active_raindrops.keys()):
            brightness = active_raindrops[led_index]["brightness"]
            direction = active_raindrops[led_index]["direction"]

            # Update the brightness
            brightness += direction

            # If the LED reaches full brightness or dims back to dim, reverse direction
            if brightness >= 255:
                brightness = 255
                direction = -20  # Start fading out
            elif brightness <= 30:
                brightness = 30  # Return to dim state and stop raindrop effect
                del active_raindrops[led_index]  # Remove the LED from active raindrops
                continue  # Skip further updates

            # Apply the updated brightness and update direction
            raindrop_brighten_fade(led_index, brightness)
            active_raindrops[led_index]["brightness"] = brightness
            active_raindrops[led_index]["direction"] = direction

        time.sleep(0.042)  # Short delay for smoother transitions



