"""
Luftdaten.at Station v2.3 LoRa ESP32
Firmware

author: Silvio Heinze (silvio@luftdaten.at)
license: MIT License
"""

from machine import I2C, Pin, UART
import bme280_i2c
import sds011
import utime
import time
from ulora import TTN, uLoRa

## read json config file
f = open('config.json', 'r')
config = ujson.loads(f.readall())

## setup bme280
scl_pin = Pin(22)
sda_pin = Pin(21)
i2c = I2C(scl=scl_pin, sda=sda_pin)
bme = bme280_i2c.BME280_I2C(address=bme280_i2c.BME280_I2C_ADDR_SEC, i2c=i2c)

bme.set_measurement_settings({
    'filter': bme280_i2c.BME280_FILTER_COEFF_16,
    'standby_time': bme280_i2c.BME280_STANDBY_TIME_500_US,
    'osr_h': bme280_i2c.BME280_OVERSAMPLING_1X,
    'osr_p': bme280_i2c.BME280_OVERSAMPLING_16X,
    'osr_t': bme280_i2c.BME280_OVERSAMPLING_2X
    })

bme.set_power_mode(bme280_i2c.BME280_NORMAL_MODE)

## setup sds011
uart=UART(1,9600)
uart.init(9600,bits=8,parity=None,stop=1,rx=2,tx=4)
pm_sensor = sds011.SDS011(uart)

## setup LoRa with TTN
LORA_CS = const(18)
LORA_SCK = const(5)
LORA_MOSI = const(27)
LORA_MISO = const(19)
LORA_IRQ = const(26)
LORA_RST = const(12)
LORA_DATARATE = "SF9BW125"

DEVADDR = config.devaddr
NWKEY = config.nwkey
APP = condig.app

TTN_CONFIG = TTN(DEVADDR, NWKEY, APP, country="EU")
FPORT = 1
lora = uLoRa(
    cs=LORA_CS,
    sck=LORA_SCK,
    mosi=LORA_MOSI,
    miso=LORA_MISO,
    irq=LORA_IRQ,
    rst=LORA_RST,
    ttn_config=TTN_CONFIG,
    datarate=LORA_DATARATE,
    fport=FPORT
)

## function (not finished)
def packPm(pm):
    pmByte = bytearray([0x0, 0x0, 0x0, 0x0])
    return pmByte


## main loop
while True:

    # Read values for PM2.5, PM10 from SDS011 sensor
    pm_sensor.read()

    # Convert PM values into LoRa packet bytes
    payloadPm25 = packPm(pm_sensor.pm25)
    payloadPm10 = packPm(pm_sensor.pm10)

    # Read values for temperature, pressure, humminidty from bme280 sensor
    temp,pa,hum = bme.get_measurement()

    payloadTemp = hex(int(temp * 2))
    payloadPa = ustruct.pack('h', pa/100)
    payloadHum = hex(int(hum))

    data = bytearray([payloadPm10[0], payloadPm10[1], 0x00, 0x00])
    lora.send_data(data, len(data), lora.frame_counter)

    # Wait for 10min (600s)
    time.sleep(600)
