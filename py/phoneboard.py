import threading
import time


import config
import tornado_server
import jk_audio
import twilio_api
import groups

def main():
    print("Welcome to phoneboard!")
    config.config()
    time.sleep(.1)

    web_t = threading.Thread(target=tornado_server.twisted)
    status_t = threading.Thread(target=jk_audio.codec_query_service)
    # vu_t = threading.Thread(target=jk_audio.codec_vu_service)
    twilio_t = threading.Thread(target=twilio_api.twilio_query_service)
    socket_t = threading.Thread(target=jk_audio.codec_ws_service)
    switch_t = threading.Thread(target=groups.switchboard_status_query_service)


    web_t.start()
    status_t.start()
    # vu_t.start()
    twilio_t.start()
    socket_t.start()
    switch_t.start()


if __name__ == '__main__':
    main()
