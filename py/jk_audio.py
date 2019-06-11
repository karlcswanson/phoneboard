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

def Codec_Service():
    print('codecs!')
