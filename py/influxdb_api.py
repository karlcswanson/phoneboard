import time

from influxdb import InfluxDBClient

import config
import twilio_api

VALUE_MAP_STATE = {
    'DISCONNECTED' : 0,
    'DIALING': 1,
    'UNKNOWN': 2,
    'CONNECTED': 3
}

VALUE_MAP_STUDIO = {
    'DISABLED' : 0,
    'OFF-AIR': 1,
    'ON-AIR': 2
}


def influx_send_channel(channel):
    conf = twilio_api.get_conference_by_name(channel.name)


    json_body = [
        {
            "measurement": "codec_status",
            "tags": {
                "name": channel.name,
            },
            # "time": channel.hook_tstamp,
            "fields": {
                "codec_status": VALUE_MAP_STATE[channel.channel_status()],
                "studio_light": VALUE_MAP_STUDIO[channel.studio_light],
                "vu": channel.vu,
                "call_start": channel.call_time(),
                "combined_status": VALUE_MAP_STATE[channel.combined_status()]
            }
        }
    ]

    if conf:
        conf_data = {
            "conf_status": conf.status(),
            "conf_time": conf.call_time(),
            "conf_name": conf.name,
            "conf_count": conf.call_count
        }
    else:
        conf_data = {
            "conf_status": 'NOCONF',
            "conf_time": '--:--:--',
            "conf_name": '',
            "conf_count": 0
        }
    json_body[0]['fields'].update(conf_data)

    client.write_points(json_body)


def setup():
    global client
    auth = config.config_tree['influxdb']
    client = InfluxDBClient(auth['host'], auth['port'], auth['user'],
                            auth['password'], auth['database'])

def main():
    config.config()


if __name__ == '__main__':
    main()
