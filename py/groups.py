import logging
import urllib.parse
import urllib.request
import time
import json
import config


import jk_audio

group_map = {
    'Live Sites': 'live',
    'Delayed Sites': 'delay'
}

codec_groups = []

group_update_list = []

class Group:
    def __init__(self, cfg):
        self.group_number = cfg['group']
        self.channels = []
        self.title = cfg['title']
        self.cfg = cfg
        self.timestamp = time.time() - 60
        self.switchboard = 'unknown'

        for channel in cfg['slots']:
            self.channels.append(jk_audio.get_channel_by_slot(channel))

    def group_json(self):
        out = []
        for channel in self.channels:
            out.append(channel.ch_json())

        return {
            'title': self.title, 'group': self.group_number, 'channels': out,
            'switchboard': self.get_switchboard_status()
        }

    def group_json_mini(self):
        return {
            'title': self.title, 'group': self.group_number,
            'switchboard': self.get_switchboard_status()
        }

    def call(self):
        for channel in self.channels:
            channel.call()

    def drop(self):
        for channel in self.channels:
            channel.drop()

    def set_studio_light(self, mode):
        for channel in self.channels:
            channel.set_studio_light(mode)

    def set_switchboard_status(self, status):
        if status in ['unknown', 'on-air', 'off-air']:
            self.switchboard = status
            self.timestamp = time.time()

        if self not in group_update_list:
            group_update_list.append(self)

    def get_switchboard_status(self):
        if (time.time() - self.timestamp) < 5:
            return self.switchboard
        else:
            return 'unknown'

    def change_switchboard_status(self, status):
        url = 'http://localhost:{}'.format(config.config_tree['switchboard_port'])
        print(url)
        req = urllib.request.Request(url)
        if status in ['off-air', 'on-air']:
            data = {group_map[self.title]: status }
            try:
                data = urllib.parse.urlencode(data).encode()
                resp = urllib.request.urlopen(req, timeout=1, data=data)

                if resp.getcode() == 200:
                    print('SUCCESS!')
                    switchboard_status_query()

            except:
                logging.warning('URL did not return 200')


def get_group(group_number):
    for group in codec_groups:
        if group.group_number == group_number:
            return group
    return None



def switchboard_status_query():
    url = 'http://localhost:{}'.format(config.config_tree['switchboard_port'])
    print(url)
    req = urllib.request.Request(url)

    try:
        resp = urllib.request.urlopen(req, timeout=1)

        if resp.getcode() == 200:
            out = json.loads(resp.read())
            print("out:{}".format(out))
            get_group(1).set_switchboard_status(out['live'])
            get_group(2).set_switchboard_status(out['delay'])

    except:
        logging.warning('switchboard URL did not return 200')

def switchboard_status_query_service():
    while True:
        switchboard_status_query()

        time.sleep(1)
