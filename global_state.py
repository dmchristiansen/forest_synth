

class GlobalState:

    def __init__(self, num_channels_=16):
        self.num_channels = num_channels_
        self.channels = [[] for _ in range(self.num_channels)]

    def listen(self, callback_fn, channel=0):
        if channel >= self.num_channels:
            print("Invalid channel number")
            return
        
        self.channels[channel].append(callback_fn)
        return
    
    def speak(self, channel=0):
        if channel >= self.num_channels:
            print("Invalid channel number")
            return

        for fn in self.channels[channel]:
            fn()