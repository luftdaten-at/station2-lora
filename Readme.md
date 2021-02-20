# Luftdaten.at Station v2.3 LoRa

## Hardware Setup


## Micropython Setup

Using esptool.py you can erase the flash with the command:
`esptool.py --port /dev/ttyUSB0 erase_flash`

And then deploy the new firmware using:
`esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20180511-v1.9.4.bin`

Once you have the firmware on the device you can access the REPL (Python prompt) over UART0 (GPIO1=TX, GPIO3=RX), which might be connected to a USB-serial convertor, depending on your board. The baudrate is 115200.


## Installation

Save config-sample.json as config.json and add the The Things Network settings.
