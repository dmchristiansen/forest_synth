
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
    return wavetable


# State machines



# Audio modules

class AudioModule:
    def __init__(self):
        self.inputs = []

    def generate_samples(self):
        return None

class AudioGenerator(AudioModule):
    def __init__(self, wave_table_gen_fn_, freq_, dynamic_wave_table_=False):
        self.wavetable = []
        self.wave_table_fn = wave_table_gen_fn_
        self.dynamic = dynamic_wave_table_
        self.frequency = freq_

        self.generate_wavetable()

    def generate_wavetable(self):
        self.wavetable = self.wave_table_fn(freq=self.frequency)

    def generate_samples(self, num_samples=global_settings.BUFFER_SIZE):
        return np.array([next(self.wavetable) for _ in range(num_samples)])


class ADSR:
    def __init__(self, gate_input_=None):
        self.gate_input = gate_input_
        self.state = "IDLE"
        self.attack = 0.3
        self.decay = 0.1
        self.sustain = 0.8
        self.release = 0.4
        self.output = 0
        self.amp = 0
        self.index = 0

    def patch_gate_input(self, input_fn):
        self.gate_input = input_fn

    def edge_detect(self, data, item):
        for index, val in np.ndenumerate(data):
            if val == item:
                return index

    def sample(self, gate):
        match self.state:
            case "IDLE":
                self.amp = 0.0
                if gate:
                    self.state = "ATTACK"
                    self.index = 0.0
                return self.amp
            case "ATTACK":
                self.amp = self.index
                self.index += 1 / (global_settings.SAMPLE_RATE * self.attack) # 1/(sample_rate*seconds)
                if self.index >= 1.0:
                    self.state = "DECAY"
                    self.index = 0.0
                if not gate:
                    self.state = "RELEASE"
                    self.index = 0
                return self.amp
            case "DECAY":
                self.amp = (1 - self.index) * (1 - self.sustain) + self.sustain
                self.index += 1 / ((self.decay / 2) * global_settings.SAMPLE_RATE)
                if self.index <= self.release:
                    self.state = "SUSTAIN"
                    self.index = 0.0
                if not gate:
                    self.state = "RELEASE"
                    self.index = 0.0
                return self.amp
            case "SUSTAIN":
                self.amp = self.sustain
                if not gate:
                    self.state = "RELEASE"
                    self.index = 0.0
                return self.amp
            case "RELEASE":
                self.amp = (1 - self.index) * self.sustain
                self.index += 1 / (self.release * 2 * global_settings.SAMPLE_RATE)
                if gate:
                    self.state = "ATTACK"
                    self.index = 0.0
                return self.amp

    def generate_samples(self, num_samples=global_settings.BUFFER_SIZE):
        gate_data = np.nditer(self.gate_input(num_samples))
        out_data = np.array([self.sample(next(gate_data)) for _ in range(num_samples)])
        return out_data


class VCA:
    def __init__(self, audio_input_=None, control_input_=None):
        self.audio_input = audio_input_
        self.control_input = control_input_

    def patch_audio_input(self, input_fn):
        self.audio_input = input_fn

    def patch_control_input(self, input_fn):
        self.control_input = input_fn

    def generate_samples(self, num_samples=global_settings.BUFFER_SIZE):
        audio_buffer = self.audio_input(num_samples)
        control_buffer = self.control_input(num_samples)
        return audio_buffer * control_buffer
    
class PulseGenerator:
    def __init__(self, pulse_length_=0.0):
        self.pulse_length = pulse_length_ # In seconds
        self.state = "LOW"

    def trigger(self):
        self.state = "HIGH"
        self.remaining_samples = self.pulse_length * global_settings.SAMPLE_RATE

    def generate_samples(self, num_samples=global_settings.BUFFER_SIZE):
        if self.state == "HIGH":
            if self.remaining_samples <= num_samples:
                data = np.array([1.0 if index < self.remaining_samples else 0.0 for index in range(num_samples)])
                self.state = "LOW"
                self.remaining_samples = 0
                return data
            else:
                self.remaining_samples -= num_samples
                return np.ones(num_samples)
        else:
            return np.zeros(num_samples)

