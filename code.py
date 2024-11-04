# SPDX-FileCopyrightText: © 2024 Gustavo Diaz <contact@gusdiaz.dev>
#
# SPDX-License-Identifier: MIT

import board
import time
import supervisor
import pwmio
import usb_hid
import json
from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

supervisor.runtime.autoreload = False

# Constants
DEBOUNCE_TIME = 0.05  # Debounce time in seconds
LED_FREQUENCY = 1000  # PWM Frequency
DUTY_CYCLE_SCALE = 65535 / 100  # PWM Duty Cycle Values

# Define the default button configuration in case of errors
default_button_pins = {
    "GP1": ["E"],
    "GP2": ["R"],
    "GP14": ["O"],
    "GP15": ["R"]
}

# Load configuration or set fallback values if no file is found
try:
    with open('keyboard_config.json', 'r') as config_file:
        config = json.load(config_file)
except (FileNotFoundError, json.JSONDecodeError) as error:
    print(f"Error loading configuration: {error}. Using default settings.")
    config = {
        "led_intensities": [100] * len(default_button_pins),
        "button_pins": default_button_pins
    }

# Debug flag
DEBUG_MODE = False

# Function to print debug messages
def debug_print(message):
    if DEBUG_MODE:
        print(message)

# Initialize onboard LED
onboard_led = DigitalInOut(board.LED)
onboard_led.direction = Direction.OUTPUT
onboard_led.value = True

# For web restart purposes
serial_state = supervisor.runtime.serial_bytes_available

# Initialize LED pins with PWM
led_pins = [board.GP28, board.GP27, board.GP17, board.GP16]
leds = [pwmio.PWMOut(pin, frequency=LED_FREQUENCY) for pin in led_pins]

# Set LED intensities from config
led_intensities = config.get("led_intensities", [100] * len(led_pins))
for led_index, (led, intensity) in enumerate(zip(leds, led_intensities)):
    led.duty_cycle = int(intensity * DUTY_CYCLE_SCALE)
    debug_print(f"LED on pin {led_pins[led_index]} set to intensity: {intensity}")

# Initialize keyboard and layout
kbd = Keyboard(usb_hid.devices)
kbd_layout = KeyboardLayoutUS(kbd)

# Preprocess button actions to determine whether each pin uses a string or keycodes
button_pins = config.get("button_pins", default_button_pins)
preprocessed_actions = {}

for pin_name, button_data in button_pins.items():
    if isinstance(button_data, dict) and "string" in button_data:
        # Store the string directly if present
        preprocessed_actions[pin_name] = {"type": "string", "value": button_data["string"]}
        debug_print(f"Pin {pin_name} will send string: {button_data['string']}")
    else:
        # Precompute keycodes if it's a list of keys
        keycodes = [getattr(Keycode, key) for key in button_data]
        preprocessed_actions[pin_name] = {"type": "keycodes", "value": keycodes}
        debug_print(f"Pin {pin_name} will send keycodes: {keycodes}")

# Initialize button pins and state tracking
pin_objects = {}
button_state = {pin_name: True for pin_name in button_pins}  # True = not pressed with pull-up

for pin_name in button_pins:
    pin = DigitalInOut(getattr(board, pin_name))
    pin.direction = Direction.INPUT
    pin.pull = Pull.UP
    pin_objects[pin_name] = pin
    debug_print(f"Initialized button pin {pin_name}")

# Main loop
while True:
    
    # Check for web serial reload command
    if supervisor.runtime.serial_bytes_available > serial_state:
        print("Reloading...")
        supervisor.reload()

    # Process each button's state
    for pin_name, action in preprocessed_actions.items():
        pin = pin_objects[pin_name]
        current_state = pin.value  # False if the button is pressed, True otherwise

        # Button press
        if not current_state and button_state[pin_name]:
            if action["type"] == "string":
                kbd_layout.write(action["value"])
                debug_print(f"String sent from {pin_name}: {action['value']}")
            else:
                for keycode in action["value"]:
                    kbd.press(keycode)
                debug_print(f"Button pressed on {pin_name}: {action['value']}")
            
            time.sleep(DEBOUNCE_TIME)  # Debounce delay

        # Button release
        elif current_state and not button_state[pin_name]:
            kbd.release_all()
            debug_print(f"Button released on {pin_name}")

        # Update the stored state
        button_state[pin_name] = current_state