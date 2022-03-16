from machine import Pin, SPI
import time, framebuf
import Screen

spi=SPI(id=1, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(10, Pin.OUT), mosi=Pin(11,Pin.OUT))

dc_pin=Pin(0,Pin.OUT)
rest_pin=Pin(1,Pin.OUT,Pin.PULL_UP)

screen = Screen.ST7032(spi, dc_pin, rest_pin, 250, 122)
screen.text('hello world', 5, 5)
screen.fill_rect(5, 20, 10, 20, 1)
screen.text('hello2 world2', 150, 50)
screen.line(5,50,220,100,1)
screen.flush_buffer()
