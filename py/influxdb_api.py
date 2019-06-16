import time

from influxdb import InfluxDBClient

import config


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
    json_body = [
        {
            "measurement": "codec_status",
            "tags": {
                "name": channel.name,
            },
            # "time": channel.hook_tstamp,
            "fields": {
                "codec_status": VALUE_MAP_STATE[channel.channel_status()],
                "studio_light": channel.studio_light,
                "vu": channel.vu,
                "call_start": channel.call_start
            }
        }
    ]

    client.write_points(json_body)

def influx_send_twilio(conference):
    json_body = [
        {
            "measurement": "twilio_status",
            "tags": {
                "name": conference.name,
            },
            # "time": channel.hook_tstamp,
            "fields": {
                "codec_status": VALUE_MAP_STATE[conference.status()],
                "call_count": conference.call_count
            }
        }
    ]

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
