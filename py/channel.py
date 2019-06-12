import time
import logging

import codec


class Channel:
    def __init__(self, codec, cfg):
        self.codec = codec
        self.name = cfg['name']
        self.channel = cfg['channel']
        self.uri = cfg['uri']
        self.timestamp = time.time() - 60
        self.slot = cfg['slot']
        self.hook_status = 'DISCONNECTED'
        self.call_start = time.time() - 60
        self.vu = 0
        self.studio_light = 'OFF_AIR'


    def set_hook_status(self, status):
        if self.hook_status == 'CONNECTED' and status == 'DISCONNECTED':
            delta = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.call_start))
            logging.info('{} is disconnected after {}'.format(self.name, delta))

        if self.hook_status != 'CONNECTED' and status == 'CONNECTED':
            self.call_start = time.time()

        if status in ['DISCONNECTED', 'DIALING', 'CONNECTED']:
            self.hook_status = status

        logging.info('{} is {}'.format(self.name, self.hook_status))

    def get_hook_status(self):
        path = '/ve/channel/ahStatus?ch=' + self.channel
        out = self.codec.load_json(path)
        if out['oh'] == 1:
            self.set_hook_status('CONNECTED')
        elif out['oh'] == 4:
            self.set_hook_status('DIALING')
        else:
            self.set_hook_status('DISCONNECTED')

        self.timestamp = time.time()


    def call(self):
        path = '/ve/channel/call?ch={}&uri={}'.format(self.channel, self.uri)
        out = self.codec.load_json(path)
        # if 'call' in out:
            # self.set_hook_status('DIALING')
        print(out)

    def drop(self):
        path = '/ve/channel/line?ch={}&oh=false'.format(self.channel)
        out = self.codec.load_json(path)
        # if out['oh'] == 0:
            # self.set_hook_status('DISCONNECTED')
        print(out)

    def call_time(self):
        if self.hook_status == 'CONNECTED':
            delta = time.time() - self.call_start
            return time.strftime('%H:%M:%S', time.gmtime(delta))

        return '--:--:--'

    def ch_json(self):
        return {
            'name': self.name, 'status': self.hook_status, 'slot': self.slot,
            'vu': self.vu, 'call_time': self.call_time()
        }
