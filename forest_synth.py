
import sequencer
import audio_engine


# Initialize sequencer
seq = sequencer.Sequencer(bpm_=212)
seq.add_track("Test 1", 8, 1, [True, False, False, True, True, True]) # Test len(gate_list) < step_count
seq.add_track("Test 2", 8, 2, [True, False, False, True, True, True, False, False]) # Test len(gate_list) = step_count
seq.add_track("Test 3", 8, 3, [True, True, False, True, True, False, True, False, True]) # Test len(gate_list) > step_count
print(seq)


# Initialize audio engine & construct synth voices
ae = audio_engine.AudioEngine()
ae.start()

# Start playing
#seq.start()

try:
    print("Starting...")
 
    while True:
        pass
       

except KeyboardInterrupt as err:


    seq.stop()
    print("Stopping...")


