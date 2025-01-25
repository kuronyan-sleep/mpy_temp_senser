# PicoW BLE Temperature Sensor

This project (picow_ble_sht31_senser.py) implements a BLE-based temperature sensor using a Raspberry Pi Pico W and MicroPython. The program reads temperature data from an SHT31 sensor via I2C and transmits the data to a PC or mobile device using Bluetooth Low Energy (BLE).

## Features

- **Temperature Measurement**: Reads temperature data from an SHT31 sensor connected via I2C.
- **BLE Communication**: Transmits the temperature data to connected devices via Bluetooth Low Energy (BLE).
- **Real-time Updates**: Sends temperature data to a PC or mobile device at regular intervals (with optional notifications).
- **MicroPython on PicoW**: Utilizes MicroPython on a Raspberry Pi Pico W board.

## Requirements

- **Hardware**:
  - Raspberry Pi Pico W
  - SHT31 temperature sensor (via I2C)
- **Software**:
  - MicroPython installed on PicoW
  - Bluetooth-enabled PC or mobile device for receiving data

## Installation

1. Clone the repository to your local machine:

   git clone https://github.com/kuronyan-sleep/mpy_temp_senser.git

2. Install MicroPython on your Raspberry Pi Pico W if not already installed. Follow the [official installation guide](https://www.raspberrypi.org/documentation/pico/getting-started/) for setting up MicroPython.

3. Flash the program to your Pico W by uploading the script to the device.

4. Connect the SHT31 temperature sensor to the I2C pins (SCL: Pin 18, SDA: Pin 19 for PicoW).

## Usage

Once the program is running on the Pico W, the device will start advertising its BLE service, and the temperature data will be sent to any connected Bluetooth-enabled device (PC, smartphone, etc.). The program will periodically send temperature updates every second.

### BLE Service UUIDs

- **Environmental Sensing Service UUID**: `0x181A`
- **Temperature Characteristic UUID**: `0x2A6E`

### Example:

If you're using a smartphone, you can connect to the device and receive real-time temperature updates. On a PC, you can use a tool like [nRF Connect](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-desktop) to connect to the Pico W and view the temperature data.

## Code Explanation

- **BLE Setup**: The program sets up a BLE service for environmental sensing (`0x181A`) and a characteristic for temperature (`0x2A6E`).
- **I2C Communication**: It reads the temperature from the SHT31 sensor using I2C. The temperature is then sent as a 16-bit integer over BLE.
- **Advertising**: The Pico W continuously advertises the environmental sensing service and allows devices to connect to it.
- **Temperature Updates**: The temperature data is updated every second and sent to any connected device, with support for notifications and indications.

## About the Code

- `picow_ble_sht31_sensor.py` is based on the official Raspberry Pi Pico W sample program `picow_ble_temp_sensor.py`. It has been modified to interface with the SHT31 sensor for temperature readings via I2C.
- `ble_advertising.py` used in this project is the official Raspberry Pi version.
- Additionally, `picow_ble_temp_reader.py` is included as a reference, based on the official Raspberry Pi sample program.
- The code is inspired by examples from the official Raspberry Pi Pico MicroPython repository: [https://github.com/raspberrypi/pico-micropython-examples/tree/master/bluetooth](https://github.com/raspberrypi/pico-micropython-examples/tree/master/bluetooth).

## Code Walkthrough

The program defines a `BLETemperature` class that manages the BLE communication and temperature reading. The main steps include:

- **I2C Communication**: The `update_temperature` method reads the temperature from the SHT31 sensor via I2C.
- **BLE Advertising**: The Pico W continuously advertises the environmental sensing service and allows devices to connect to it.
- **Notifications and Indications**: The `update_temperature` method optionally sends notifications or indications to connected devices with the latest temperature data.

## License

This project is licensed under the MIT License.
