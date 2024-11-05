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

To set up your keyboard, you can use the web configurator at [https://keyboard-manager.gusdiaz.dev](https://keyboard-manager.gusdiaz.dev). Simply load the configuration file from the root of your board and connect using Web Serial. The UI will guide you through assigning keys and customizing settings.

Alternatively, you can configure manually by editing the keyboard_config.json file. Define button actions and LED intensities, where each button can be mapped to:
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

## Development Tools

For editing and managing files on your RP2040 board, I recommend using either [ViperIDE](https://viper-ide.org/) or [Thonny](https://thonny.org/):

- **ViperIDE**: An web-based IDE designed for microcontroller programming. ViperIDE offers a clean interface and tools tailored for MicroPython and CircuitPython development.
- **Thonny**: An easy-to-use Python IDE with built-in support for CircuitPython and MicroPython. It allows you to edit files directly on the board, view the serial output, and install libraries.

Both tools provide straightforward access to the board’s filesystem, making it easier to edit your `keyboard_config.json` and `code.py` files, manage libraries, and debug code in real-time.


## Troubleshooting
Ensure the keyboard_config.json file is properly formatted.
Check connections for all buttons and LEDs.
Confirm required libraries are installed on the CircuitPython filesystem.

## License
This project is open-source and available under the MIT License.
