import global_settings
import sequencer
import audio_engine
import queue

# Intitalize global task queue
task_queue = queue.Queue()

# Initialize sequencer
seq = sequencer.Sequencer(bpm_=212)
seq.add_track("Test 1", 8, 1, [True, False, False, True, True, True]) # Test len(gate_list) < step_count
seq.add_track("Test 2", 8, 2, [True, False, False, True, True, True, False, False]) # Test len(gate_list) = step_count
seq.add_track("Test 3", 8, 3, [True, True, False, True, True, False, True, False, True]) # Test len(gate_list) > step_count
print(seq)

# Initialize audio engine & construct synth voices
ae = audio_engine.AudioEngine(task_queue)
for _ in range(global_settings.AUDIO_BUFFER_COUNT - 1):
    ae.get_samples()
print(ae.buffer.buffer[0])

try:
    print("Starting...")
    ae.start()
    #seq.start()

    while True:
        if task_queue.empty() is False:
            task = task_queue.get()
            if task is not None:
                match task:
                    case "GET_SAMPLES":
                        print("\nCalling 'get samples'")
                        ae.get_samples()                        

       

except KeyboardInterrupt as err:


    seq.stop()
    print("Stopping...")


