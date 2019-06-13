import time

from codec import Codec


audio_codecs = []

def get_codec_by_ip(ip):
    return next((x for x in audio_codecs if x.ip == ip), None)

def check_add_codec(ip):
    net = get_codec_by_ip(ip)
    if net:
        return net

    net = Codec(ip)
    audio_codecs.append(net)
    return net

def get_channel_by_slot(slot):
    for codec in audio_codecs:
        for channel in codec.channels:
            if channel.slot == slot:
                return channel
    return None

def codec_query_service():
    while True:
        for codec in audio_codecs:
            for channel in codec.channels:
                channel.get_hook_status()
                if channel.studio_light == 'ON-AIR' and channel.hook_status == 'DISCONNECTED':
                    channel.call()
                if channel.studio_light == 'OFF-AIR' and channel.hook_status == 'CONNECTED':
                    channel.drop()
        time.sleep(1)



def codec_vu_service():
    while True:
        for codec in audio_codecs:
            codec.get_vu()
        time.sleep(.3)
