
"""


"""

import math
import itertools
import pyaudio
import numpy as np
import global_settings

# Simple sound generators

def get_sin_oscillator(freq=55, amp=1, sample_rate=global_settings.SAMPLE_RATE):
    increment = (2 * math.pi * freq) / sample_rate
    wavetable = (math.sin(v) * amp for v in itertools.count(start=0, step=increment))
    #print("\nLength of wavetable: " + str(len(wavetable)))
    return wavetable


# State machines



# Audio modules

class AudioModule:
    def __init__(self):
        self.inputs = []

    def generate_samples(self):
        return None

class AudioGenerator(AudioModule):
    def __init__(self, wave_table_gen_fn_, freq_, dynamic_=False):
        self.wavetable = []
        self.wave_table_fn = wave_table_gen_fn_
        self.dynamic = dynamic_
        self.frequency = freq_

        self.generate_wavetable()

    def generate_wavetable(self):
        self.wavetable = self.wave_table_fn(freq=self.frequency)

    def generate_samples(self, num_samples=global_settings.BUFFER_SIZE):
        return [next(self.wavetable) for _ in range(num_samples)]

class AudioModifier(AudioModule):
    def __init__(self):
        pass





