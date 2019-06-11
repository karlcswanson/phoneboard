import time

import codec


class Channel:
    def __init__(self, codec, cfg):
        self.codec = codec
        self.timestamp = time.time() - 60
        self.slot = cfg['slot']
    
