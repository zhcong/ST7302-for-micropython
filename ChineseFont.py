import gc

GC_RATE = 100

class ChineseFont:
    
    def __init__(self, file, collect):
        # open data file
        self.__collect = collect
        self.__db_file = open(file, 'rb')
        self.__load_map()
    
    def get_font_size(self):
        return self.__font_size

    def is_exist(self, key):
        return key in self.__map
    
    def get_font_count(self):
        return self.__font_count
    
    # get bit map
    def get_bit_map(self, key):
        if not self.is_exist(key):
            return bytearray()
        sort = self.__map[key]
        self.__db_file.seek(2 + 4 + int((self.__font_size * self.__font_size) / 8) * sort)
        return self.__db_file.read(int((self.__font_size * self.__font_size) / 8))

    def close(self):
        self.__db_file.close()
    
    def __load_map(self):
        # font_size
        font_size_byte = self.__db_file.read(2)
        self.__font_size = int.from_bytes(font_size_byte, 'big')
        # font_count
        font_count_byte = self.__db_file.read(4)
        self.__font_count = int.from_bytes(font_count_byte, 'big')
        # seek
        self.__db_file.seek(int((self.__font_size * self.__font_size * self.__font_count) / 8) + 4 + 2)
        # load map
        self.__map = {}
        load_count = 0
        while True:
            key_len = self.__db_file.read(1)
            if key_len == b'':
                break
            if(key_len[0] == 1):
                key = self.__db_file.read(1)
            else:
                key = self.__db_file.read(3)
            data = self.__db_file.read(4)
            self.__map[key.decode('utf-8')] = int.from_bytes(data, 'big')
            if self.__collect and load_count % GC_RATE == 0:
                gc.collect()
            load_count = load_count + 1
