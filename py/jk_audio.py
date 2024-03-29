import time
import logging

from codec import Codec
from channel import data_update_list
# import influxdb_api

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
                channel.get_hook_status_from_codec()
                conf = channel.conf()
                if channel.studio_light == 'ON-AIR' and channel.hook_status == 'DISCONNECTED':
                    channel.call()

                if channel.studio_light == 'OFF-AIR' and channel.hook_status == 'CONNECTED':
                    channel.drop()


                if conf:
                    if channel.studio_light == 'ON-AIR' and conf.status() in ['OPEN', 'DISCONNECTED']:
                        if channel.hook_status == 'CONNECTED':
                            if (time.time() - channel.call_start) > 20:
                                channel.drop()

                    if channel.studio_light == 'OFF-AIR' and conf.status() in ['OPEN', 'CONNECTED']:
                        conf.close_room()

                if not conf and channel.studio_light == 'ON-AIR':
                    if channel.hook_status == 'CONNECTED':
                        if (time.time() - channel.call_start) > 20:
                            channel.drop()

                # if channel.studio_light == 'ON-AIR' and channel.hook_status == 'CONNECTED':
                #     if (time.time() - channel.call_start) > 14400:
                #         channel.drop()
                # influxdb_api.influx_send_channel(channel)

        time.sleep(1)

def codec_ws_service():
    time.sleep(2)
    while True:
        for codec in audio_codecs:
            for channel in codec.channels:
                if channel not in data_update_list:
                    data_update_list.append(channel)
        time.sleep(1)


def codec_vu_service():
    while True:
        for codec in audio_codecs:
            codec.get_vu()
        time.sleep(.3)
