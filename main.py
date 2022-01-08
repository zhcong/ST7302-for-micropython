from machine import Pin, SPI
import time, framebuf
import Screen
from ChineseFont import ChineseFont

spi=SPI(id=1, baudrate=5_000_000, polarity=0, phase=0, sck=Pin(10, Pin.OUT), mosi=Pin(11,Pin.OUT))

dc_pin=Pin(0,Pin.OUT)
rest_pin=Pin(1,Pin.OUT,Pin.PULL_UP)

screen = Screen.ST7032(spi, dc_pin, rest_pin, 250, 122)
font = ChineseFont('font_32.data', True)
framebuffer = framebuf.FrameBuffer(bytearray(font.get_bit_map('言')), 32, 32, framebuf.MONO_HLSB)
screen.blit(framebuffer,10,10)
framebuffer = framebuf.FrameBuffer(bytearray(font.get_bit_map('一')), 32, 32, framebuf.MONO_HLSB)
screen.blit(framebuffer,42,10)
framebuffer = framebuf.FrameBuffer(bytearray(font.get_bit_map('小')), 32, 32, framebuf.MONO_HLSB)
screen.blit(framebuffer,74,10)
framebuffer = framebuf.FrameBuffer(bytearray(font.get_bit_map('狗')), 32, 32, framebuf.MONO_HLSB)
screen.blit(framebuffer,106,10)
framebuffer = framebuf.FrameBuffer(bytearray(font.get_bit_map('狗')), 32, 32, framebuf.MONO_HLSB)
screen.blit(framebuffer,138,10)
screen.flush_buffer()