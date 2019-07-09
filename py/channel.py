import time
import logging


import twilio_api
import codec


data_update_list = []

class CodecChannel:
    def __init__(self, codec, cfg):
        self.codec = codec
        self.name = cfg['name']
        self.channel = cfg['channel']
        self.uri = cfg['uri']
        self.hook_tstamp = time.time() - 60
        self.slot = cfg['slot']
        self.hook_status = 'UNKNOWN'
        self.call_start = time.time() - 60
        self.vu = 0
        self.studio_light = 'DISABLED'
        self.drops = 0
        self.call_drop_tstamp = time.time() - 60


    def set_studio_light(self, mode):
        if self.studio_light != mode:
            self.drops = 0


        if mode in ['DISABLED', 'OFF-AIR', 'ON-AIR']:
            self.studio_light = mode


    def set_hook_status(self, status):
        if self.hook_status == 'CONNECTED' and status == 'DISCONNECTED':
            delta = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.call_start))
            logging.info('{} is disconnected after {}'.format(self.name, delta))

        if self.hook_status != 'CONNECTED' and status == 'CONNECTED':
            self.call_start = time.time()

        if status in ['DISCONNECTED', 'DIALING', 'CONNECTED']:
            self.hook_status = status

        logging.info('{} is {}'.format(self.name, self.hook_status))

    def get_hook_status_from_codec(self):
        path = '/ve/channel/ahStatus?ch=' + self.channel
        out = self.codec.load_json(path)
        if out:
            if out['oh'] == 1:
                self.set_hook_status('CONNECTED')
            elif out['oh'] == 4:
                self.set_hook_status('DIALING')
            else:
                self.set_hook_status('DISCONNECTED')

            self.hook_tstamp = time.time()
        # if self not in data_update_list:
        #     data_update_list.append(self)

    def channel_status(self):
        if (time.time() - self.hook_tstamp) < 4:
            return self.hook_status
        return 'UNKNOWN'

    def call(self):
        if time.time() - self.call_drop_tstamp < 4:
            return None

        path = '/ve/channel/call?ch={}&uri={}'.format(self.channel, self.uri)
        out = self.codec.load_json(path)
        self.call_drop_tstamp = time.time()

        if self.conf():
            self.drops = self.drops + 1


    def drop(self):
        path = '/ve/channel/line?ch={}&oh=false'.format(self.channel)
        out = self.codec.load_json(path)

    def call_time(self):
        if self.hook_status == 'CONNECTED':
            delta = time.time() - self.call_start
            return time.strftime('%H:%M:%S', time.gmtime(delta))

        return '--:--:--'

    def conf(self):
        print("LOOKING FOR: {}".format(self.name))
        conf = twilio_api.get_conference_by_name(self.name)
        if conf:
            return conf
        return None

    def combined_status(self):
        conf = self.conf()
        if conf:
            if conf.status() == 'CONNECTED' and self.channel_status() == 'CONNECTED':
                return 'CONNECTED'

            if conf.status() == 'CONNECTED' and self.channel_status() in ['DISCONNECTED', 'DIALING']:
                return 'OPEN'

            if conf.status() == 'UNKNOWN':
                return 'UNKNOWN'

        if self.channel_status() == 'UNKNOWN':
            return 'UNKNOWN'

        return 'DISCONNECTED'

    def ch_json(self):
        json_out = {
            'name': self.name, 'codec_status': self.channel_status(),
            'slot': self.slot, 'ip': self.codec.ip, 'vu': self.vu,
            'drops': self.drops,
            'call_time': self.call_time(), 'studio_light': self.studio_light,
            'status': self.combined_status()
        }
        conf = self.conf()
        if conf:
            conf_out = {
                'conf_status': conf.status(), 'conf_time': conf.call_time(),
                'conf_name': conf.name, 'conf_count': conf.call_count
            }
        elif twilio_api.conn.is_connected():
            conf_out = {
                'conf_status': 'DISCONNECTED', 'conf_time': '--:--:--',
                'conf_name': '', 'conf_count': 0
            }
        else:
            conf_out = {
                'conf_status': 'UNKNOWN', 'conf_time': '--:--:--',
                'conf_name': '', 'conf_count': 0
            }
        json_out.update(conf_out)
        return json_out
