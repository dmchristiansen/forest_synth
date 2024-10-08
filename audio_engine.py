"""
audio_engine.py

Class to represent a voice object that holds information about synthesis, generation


"""

import math
import itertools
import pyaudio
import numpy as np
import global_settings
import audio_modules
import global_state
import buffer





class SynthVoice:
    def __init__(self):
        pass

class AudioEngine:
    
    def __init__(self, queue_, global_state_):
        self.stream = None
        self.voices = []
        self.voice_count = 0
        self.queue = queue_
        self.state = global_state_
        self.audio_output = None
        
        self.buffer = buffer.Buffer(global_settings.AUDIO_BUFFER_COUNT)

    def start(self):
        self.stream = pyaudio.PyAudio().open(
            rate=global_settings.SAMPLE_RATE,
            channels=1,
            format=pyaudio.paInt16,
            output=True,
            frames_per_buffer=global_settings.BUFFER_SIZE,
            stream_callback=self.audio_buffer_callback
        )

    def close(self):
        self.stream.close()

    def get_samples(self, num_samples=global_settings.BUFFER_SIZE):
        data = self.audio_output(num_samples)
        data = np.int16(data.clip(-0.8, 0.8) * 32767)
        self.buffer.fill_buffer(data)
        return
    
    def audio_buffer_callback(self, input_data, frame_count, time_info, status_flags):
        self.queue.put("GET_SAMPLES")
        return (self.buffer.get_buffer(), pyaudio.paContinue)

    def add_voice(self, module):
        self.voices.append(module)
        self.voice_count += 1
        return self.voices[-1].generate_samples

