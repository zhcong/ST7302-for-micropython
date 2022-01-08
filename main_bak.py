from machine import Pin, UART, SPI
import time, Screen, gc
from machine import Timer
import framebuf
from ChineseFont import ChineseFont

# sreen
SHOW_TIME_MS = 30000
FONT_SIZE = 16
SCREEN_WIDTH = 128
SCREEN_HIGHT = 64
MAX_COUNT = int(SCREEN_WIDTH / FONT_SIZE * SCREEN_HIGHT / FONT_SIZE)
LINE_COUNT = int(SCREEN_WIDTH / FONT_SIZE)

font = None
screen = None
# timer
timer = Timer()
# uart
uart = UART(1, baudrate=9600)

def get_char_bits(char):
    char_bits = font.get_bit_map(char)
    return framebuf.FrameBuffer(bytearray(char_bits), FONT_SIZE, FONT_SIZE, framebuf.MONO_HLSB)

def print_words(words):
    screen.clear()
    for i, char in enumerate(words):
        char_bits_buf = get_char_bits(char)
        screen.blit(char_bits_buf, (i % LINE_COUNT) * FONT_SIZE, int(i / LINE_COUNT) * FONT_SIZE)
    screen.show()
    gc.collect()

def clear(timer):
    screen.clear()

def pin_clear(pin):
    screen.clear()

def init():
    global screen, font
    # width:128, height:64, dc-->pin1, res-->pin0
    spi=SPI(0, baudrate=115200)
    screen = Screen.create(128, 64, spi, Pin(1,Pin.OUT), Pin(0,Pin.OUT))
    screen.print('loading font.')
    font = ChineseFont('font_16.data', True)
    screen.print('load font over.')
    time.sleep(1)
    screen.clear()
    Pin(16, Pin.IN).irq(trigger=Pin.IRQ_FALLING, handler=pin_clear)

if __name__ == '__main__':
    init()
    while True:
        if uart.any():
            # timer.deinit()
            data = uart.readline()
            print_words(data.decode('utf-8').replace('\r\n', '').replace('^@', ''))
            # timer.init(period=SHOW_TIME_MS, mode=Timer.ONE_SHOT, callback=clear)