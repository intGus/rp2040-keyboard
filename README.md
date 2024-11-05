# USB HID Keyboard with Configurable Key Mapping

This project is a USB HID keyboard program written in CircuitPython, designed to run on RP2040-based boards (e.g., Raspberry Pi Pico). The keyboard configuration is read from a JSON file, allowing for flexible key mappings, custom strings, and LED intensity settings.

## Features
- Configurable key mappings and custom strings for each button
- LED intensity control for each connected LED
- Debounce timing to prevent accidental key repeats

## Hardware Requirements
- RP2040-based microcontroller (e.g., Raspberry Pi Pico)
- Buttons connected to specified GPIO pins
- LEDs connected to specific GPIO pins for PWM control (optional)

## Software Setup
1. **Install CircuitPython** on the RP2040 board.
2. **Libraries Required**:
   - `adafruit_hid` (for USB HID keyboard functionality)
   - `adafruit_dotstar.mpy`

3. **File Structure**:
   (Both files should be on the root of the device)
   - `code.py`: The main script to run on the device.
   - `keyboard_config.json`: Configuration file for key mappings and LED intensities.

## Configuration

Edit the `keyboard_config.json` file to define button actions and LED intensities. Each button can be mapped to either:
- **Keycodes**: Specify an array of key names (e.g., `"CONTROL", "C"`)
- **String**: Specify a string that will be typed when the button is pressed (e.g., `"Hello, World!"`).

Example `keyboard_config.json`:
```json
{
  "button_pins": {
    "GP1": {"string": "Hello, World!"},
    "GP2": ["CONTROL", "C"],
    "GP14": ["CONTROL", "A"],
    "GP15": {"string": "Custom Text"}
  },
  "led_intensities": [1, 70, 1, 1]
}
```

## Usage
Load the code and keyboard_config.json file onto the RP2040 board.
Connect buttons and LEDs to the GPIO pins as specified in the configuration.
Upon pressing a button, the specified keycodes or string will be sent to the connected computer.

## Troubleshooting
Ensure the keyboard_config.json file is properly formatted.
Check connections for all buttons and LEDs.
Confirm required libraries are installed on the CircuitPython filesystem.

## License
This project is open-source and available under the MIT License.
