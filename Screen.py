import time, math, framebuf

class ST7032(framebuf.FrameBuffer):
    # TODO 电压不稳
    # TODO 简化代码逻辑

    def __init__(self, spi, dc_pin, rest_pin, width, height):
        self.spi = spi
        self.rest_pin = rest_pin
        self.dc_pin = dc_pin
        # buffer max 7.5kb
        self.buffer = bytearray(math.ceil(height/8)*(width if width%2==0 else width+1))
        self.width = width
        self.height = height
        self.bit_column_fill = [ 0x00 for _ in range(3-math.ceil(height%12/4))] # once param must 3 bit
        super().__init__(self.buffer, width, height, framebuf.MONO_VLSB)
        self.init_lcd()

    def __sleep_waith_command(self, sleep_time=100):
        time.sleep_ms(sleep_time)
    
    def get_buffer(self):
        return self.buffer

    def inv_off(self):
        self.send_command(0x20)
        self.__sleep_waith_command()
    
    def inv_on(self):
        self.send_command(0x21)
        self.__sleep_waith_command()
    
    def hard_rest(self):
        self.rest_pin.value(0)
        self.__sleep_waith_command(200)
        self.rest_pin.value(1)
    
    def soft_reset(self):
        self.send_command(0xB9)  #enable CLR RAM
        self.send_param(0xE3 + self.width)
        self.__sleep_waith_command()
        self.send_command(0xB9)  #disable CLR RAM
        self.send_param(0x23) 

    def send_command(self, command):
        self.dc_pin.value(0)
        data = bytearray(1)
        data[0]=command
        self.spi.write(data)
        self.dc_pin.value(1)

    def send_param(self, param):
        data = bytearray(1)
        data[0]=param
        self.spi.write(data)

    def __shift_buffer(self, new_pos, cache):
        self.send_command(0x2a) # Row set
        self.send_param(0x19) # 0x19 is access memory start
        self.send_param(0x19+self.width)
        self.send_command(0x2b) # column set
        self.send_param(new_pos)
        self.send_param(self.height)
        self.send_command(0x2c) # write memory
        for item in cache:
            self.send_param(item)

    def flush_buffer(self):
        column_list = [[] for _ in range(self.width)]
        for i,bit in enumerate(self.buffer):
            column_list[i%self.width].append(bit)
        # TODO not append
        for column_i in range(0, len(column_list), 2):
            two_column_cache=[]
            for bit_i, bit in enumerate(column_list[column_i]):
                bit1 = self.__mix_bit(bit, column_list[column_i+1][bit_i])
                two_column_cache.append(bit1)
                bit2 = self.__mix_bit(bit>>4, column_list[column_i+1][bit_i]>>4)
                two_column_cache.append(bit2)
            self.__shift_buffer(column_i//2, two_column_cache + [0x00, 0x00])

    def __mix_bit(self, bit1:int, bit2:int):
        mix_bit=0x00
        mix_bit=mix_bit|((bit1&0x01)<<7)
        mix_bit=mix_bit|((bit2&0x01)<<6)
        mix_bit=mix_bit|((bit1&0x02)<<4)
        mix_bit=mix_bit|((bit2&0x02)<<3)
        mix_bit=mix_bit|((bit1&0x04)<<1)
        mix_bit=mix_bit|((bit2&0x04)<<0)
        mix_bit=mix_bit|((bit1&0x08)>>2)
        mix_bit=mix_bit|((bit2&0x08)>>3)
        return mix_bit

    def init_lcd(self):
        self.spi.init()
        self.hard_rest()
        self.send_command(0xeb) # Enable OTP
        self.send_param(0x02)
        self.send_command(0xd7) # OTP Load Control
        self.send_param(0x68)
        self.send_command(0xb4)  #GateEQSettingHPMEQLPMEQ
        self.send_param(0xa5)
        self.send_param(0x66)
        self.send_param(0x01)
        self.send_param(0x00)
        self.send_param(0x00)
        self.send_param(0x40)
        self.send_param(0x01)
        self.send_param(0x00)
        self.send_param(0x00)
        self.send_param(0x40)
        self.send_command(0x11) # sleep out
        self.__sleep_waith_command()
        self.send_command(0x36) # Memory Data Access Control
        self.send_param(0x00)
        self.send_command(0x39) # Low power
        self.send_command(0x3a) # DataFormatSelect4writefor24bit
        self.send_param(0x11)
        self.send_command(0xb0)  # Duty setting
        self.send_param(0x64)  # 250duty/4=63
        self.send_command(0xb8)  # Panel Setting Frame inversion
        self.send_param(0x09)  # 250duty/4=63
        self.send_command(0x29) # Display on

        self.soft_reset()

        
