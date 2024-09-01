import global_settings
import sequencer
import audio_modules
import audio_engine
import queue
import global_state
import pyaudio
import timeit
import time

class ForestSynth:
    def __init__(self):

        print("pyaudio version:" + pyaudio.__version__)

        self.state = global_state.GlobalState()

        # Intitalize global task queue
        self.task_queue = queue.Queue()

        # Initialize sequencer
        self.seq = sequencer.Sequencer(self.state, bpm_=212)
        # Test len(gate_list) < step_count
        self.seq.add_track(
            track_name="Test 1",
            step_count=8,
            step_size=1,
            channel=0,
            gate_list=[True, False, False, True, True, True])
        """
        # Test len(gate_list) = step_count
        self.seq.add_track(
            track_name="Test 2",
            step_count=8,
            step_size=2,
            channel=1,
            gate_list=[True, False, False, True, True, True, False, False])
        # Test len(gate_list) > step_count
        self.seq.add_track(
            track_name="Test 3",
            step_count=8,
            step_size=3,
            channel=2,
            gate_list=[True, True, False, True, True, False, True, False, True])
        """
        print(self.seq)

        # Initialize audio engine & construct synth voices
        self.ae = audio_engine.AudioEngine(self.task_queue, self.state)


        osc_signal = self.ae.add_voice(
            audio_modules.AudioGenerator(
                wave_table_gen_fn_=audio_modules.get_sin_oscillator,
                freq_=220
            )
        )

        lfo_signal = self.ae.add_voice(
            audio_modules.AudioGenerator(
                wave_table_gen_fn_=audio_modules.get_sin_oscillator,
                freq_=10
            )
        )
        vca1_signal = self.ae.add_voice(
            audio_modules.VCA(
                audio_input_=osc_signal,
                control_input_=lfo_signal
            )
        )
        pulse_gen = audio_modules.PulseGenerator(
            pulse_length_=0.25,
        )
        self.ae.state.listen(pulse_gen.trigger, 0)
        pulse_signal = self.ae.add_voice(pulse_gen)

        env_signal = self.ae.add_voice(
            audio_modules.ADSR(
                gate_input_=pulse_signal
            )
        )

        self.ae.audio_output = self.ae.add_voice(
            audio_modules.VCA(
                audio_input_=vca1_signal,
                control_input_=env_signal
            )
        )

        print(self.ae.buffer.buffer[0])
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

    def run(self):

        for _ in range(global_settings.AUDIO_BUFFER_COUNT - 1):
            self.ae.get_samples()

        try:
            print("Starting...")
            self.ae.start()
            #self.seq.start()

            while True:
                if self.task_queue.empty() is False:
                    task = self.task_queue.get()
                    match task:
                        case "GET_SAMPLES":
                            self.ae.get_samples()                        

        except KeyboardInterrupt as err:

            self.seq.stop()
            print("Stopping...")


