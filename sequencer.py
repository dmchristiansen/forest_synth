
"""
sequencer.py

Class object to time & fire notes

Takes input from global state object
Sends note events (midi?) to sound engine

"""
from threading import Timer

class SequencerTrack:
    def __init__(self, track_number_, track_name_, step_count_, step_size_, channel_=0, gate_list_=None):
        self.track_number = track_number_
        self.track_name = track_name_
        self.step_count = step_count_
        self.step_size = step_size_
        self.current_step = 0
        self.channel = channel_
        if gate_list_ != None:
            if self.step_count > len(gate_list_):
                self.gate_list = gate_list_ + [False for x in (0, self.step_count - len(gate_list_))]
            else:
                self.gate_list = gate_list_
        else:
            self.gate_list = [False for x in (0, self.step_count)]
        print("\nGate list: ")
        print(self.gate_list)

    def step(self):
        self.current_step = (self.current_step + self.step_size) % self.step_count

    def fire(self, fn):
        if self.gate_list[self.current_step]:
            fn(self.channel)



class Sequencer:
    def __init__(self, global_state_, bpm_ = 212):
        """
        
        """
        self.bpm = bpm_
        self.tracks = []
        self.track_count = 0
        self.is_active = False
        self.timer = None
        self.state = global_state_

    def add_track(self, track_name, step_count, step_size, channel, gate_list=None):
        """
        
        """
        self.tracks.append(SequencerTrack(self.track_count, track_name, step_count, step_size, channel, gate_list))
        self.track_count += 1

    def step_callback(self):
        self.timer = Timer(60/self.bpm, self.step_callback)
        self.timer.start()

        for track in self.tracks:
            track.step()
            track.fire(self.state.speak)


    def start(self):
        print("\nTimer set to " + str(60/self.bpm))
        self.is_active = True
        self.timer = Timer(60/self.bpm, self.step_callback)
        self.timer.start()

    def stop(self):
        self.is_active = False
        if self.timer is not None:
            self.timer.cancel()

    def reset(self):
        if self.timer is not None:
            self.timer.cancel()
        self.timer = Timer(60/self.bpm, self.step_callback, args=[self])

        # Reset all tracks to initial step

        # Play notes




