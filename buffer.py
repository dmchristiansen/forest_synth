import numpy as np
import global_settings

# Add bounds checking!

class Buffer:
    def __init__(self, buffer_count_):
        self.buffer_count = buffer_count_
        self.head = 0
        self.tail = 0
        temp = np.zeros([global_settings.BUFFER_SIZE])
        self.buffer = [temp for _ in range(self.buffer_count)]
        return

    def get_buffer(self):
        self.tail = (self.tail + 1) % self.buffer_count
        return self.buffer[self.tail]
    
    def fill_buffer(self, data):
        self.buffer[self.head] = data
        self.head = (self.head + 1) % self.buffer_count
        return