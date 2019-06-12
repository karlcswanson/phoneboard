import logging
import jk_audio

codec_groups = []

class Group:
    def __init__(self, cfg):
        self.group_number = cfg['group']
        self.channels = []
        self.title = cfg['title']
        self.cfg = cfg

        for channel in cfg['slots']:
            self.channels.append(jk_audio.get_channel_by_slot(channel))

    def group_json(self):
        out = []
        for channel in self.channels:
            out.append(channel.ch_json())

        return {
            'title': self.title, 'group': self.group_number, 'channels': out
        }

    def call(self):
        for channel in self.channels:
            channel.call()

    def drop(self):
        for channel in self.channels:
            channel.drop()


def get_group(group_number):
    for group in codec_groups:
        if group.group_number == group_number:
            return group
    return None
