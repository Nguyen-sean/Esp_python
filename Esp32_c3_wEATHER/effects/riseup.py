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
def running_strip(color, duration):
    """Function to create a fast-running strip effect for a total duration."""
    
    running_length = 60  # Total number of LEDs in the running effect
    if running_length > num_leds:
        running_length = num_leds  # Adjust if more than available LEDs

    # Calculate the number of cycles needed to fill the duration
    total_iterations = duration / 0.007  # Delay for smooth transition
    iterations_per_led = total_iterations / running_length  # How many iterations per LED

    for i in range(int(running_length * iterations_per_led)):
        # Set the color for the current LED
        np[i % num_leds] = color  # Use modulo to wrap around
        np.write()  # Update the LED strip
        time.sleep(0.00042)  # Delay for smooth transition

        # Turn off the previous LED to create a running effect
        np[(i - 20) % num_leds] = (0, 0, 0)

    # Reset all LEDs after one complete cycle
    np.fill((0, 0, 0))
    np.write()


def wave_effect(colors, duration):
    """Function to create a fast-running strip effect with multiple colors for a total duration."""
    
    running_length = 60  # Total number of LEDs in the running effect
    if running_length > num_leds:
        running_length = num_leds  # Adjust if more than available LEDs

    # Calculate the number of cycles needed to fill the duration
    total_iterations = duration / 0.007  # Delay for smooth transition
    iterations_per_led = total_iterations / running_length  # How many iterations per LED

    for i in range(int(running_length * iterations_per_led)):
        # Set the color for the current LED from the colors list
        color_index = (i // 20) % len(colors)  # Determine which color to use
        np[i % num_leds] = colors[color_index]  # Use modulo to wrap around
        np.write()  # Update the LED strip
        time.sleep(0.00042)  # Delay for smooth transition

        # Turn off the previous LED to create a running effect
        np[(i - 20) % num_leds] = (0, 0, 0)

    # Reset all LEDs after one complete cycle
    np.fill((0, 0, 0))
    np.write()

# Function to glow up to a color and stay
def glow_up(color, duration):
    """Function to create a glowing effect."""
    for brightness in range(0, 256, 1):  # Gradually increase brightness
        np.fill(tuple(int(c * (brightness / 255)) for c in color))
        np.write()
        time.sleep(0.002)  # Adjust for speed
    time.sleep(2)
    for brightness in range(255, 0, -1):  # Gradually increase brightness
        np.fill(tuple(int(c * (brightness / 255)) for c in color))
        np.write()
        time.sleep(0.002)  # Adjust for speed



def play_effect():
    """Function to run the combined effects in sequence."""
    print(f"Rise up")
    
    # Define your colors
    red = (255, 0, 10)        # Red
    purple = (255, 10, 255)  # Purple
    blue = (70, 0, 255)		# Blue
    white = (255,255,255)
    
    running_strip(red, 2)
    running_strip(blue, 2)
    # Define your colors
    colors = [
        red,   # Red
        purple,   # Purple
        blue    # Blue
    ]
    # Call the function with the colors and desired duration
    wave_effect(colors, duration=3)  # Duration in seconds
    running_strip(purple,3)
    glow_up(purple, 3)

    