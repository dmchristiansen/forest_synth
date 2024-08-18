import global_settings
import sequencer
import audio_modules
import audio_engine
import queue
import global_state
import pyaudio
import timeit
import time

print("pyaudio version:" + pyaudio.__version__)

state = global_state.GlobalState()

# Intitalize global task queue
task_queue = queue.Queue()

# Initialize sequencer
seq = sequencer.Sequencer(state, bpm_=212)
# Test len(gate_list) < step_count
seq.add_track(
    track_name="Test 1",
    step_count=8,
    step_size=1,
    channel=0,
    gate_list=[True, False, False, True, True, True])
"""
# Test len(gate_list) = step_count
seq.add_track(
    track_name="Test 2",
    step_count=8,
    step_size=2,
    channel=1,
    gate_list=[True, False, False, True, True, True, False, False])
# Test len(gate_list) > step_count
seq.add_track(
    track_name="Test 3",
    step_count=8,
    step_size=3,
    channel=2,
    gate_list=[True, True, False, True, True, False, True, False, True])
"""
print(seq)

# Initialize audio engine & construct synth voices
ae = audio_engine.AudioEngine(task_queue, state)


osc_signal = ae.add_voice(
    audio_modules.AudioGenerator(
        wave_table_gen_fn_=audio_modules.get_sin_oscillator,
        freq_=220
    )
)

lfo_signal = ae.add_voice(
    audio_modules.AudioGenerator(
        wave_table_gen_fn_=audio_modules.get_sin_oscillator,
        freq_=10
    )
)
vca1_signal = ae.add_voice(
    audio_modules.VCA(
        audio_input_=osc_signal,
        control_input_=lfo_signal
    )
)
pulse_gen = audio_modules.PulseGenerator(
    pulse_length_=0.25,
)
ae.state.listen(pulse_gen.trigger, 0)
pulse_signal = ae.add_voice(pulse_gen)

env_signal = ae.add_voice(
    audio_modules.ADSR(
        gate_input_=pulse_signal
    )
)

ae.audio_output = ae.add_voice(
    audio_modules.VCA(
        audio_input_=vca1_signal,
        control_input_=env_signal
    )
)

print(ae.buffer.buffer[0])
"""
def test_code():
    ae.get_samples()


#time = timeit.timeit(test_code)
start = time.time()
ae.get_samples()
end = time.time()

print("get_samples time(ms): ")
print((end-start)*1000)
"""

for _ in range(global_settings.AUDIO_BUFFER_COUNT - 1):
    ae.get_samples()




try:
    print("Starting...")
    ae.start()
    seq.start()

    while True:
        if task_queue.empty() is False:
            task = task_queue.get()
            match task:
                case "GET_SAMPLES":
                    ae.get_samples()                        

       

except KeyboardInterrupt as err:


    seq.stop()
    print("Stopping...")


