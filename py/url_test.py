import config
import jk_audio
import time

config.config()

# print(audio_codecs[0].channels[0].hook_status)
time.sleep(5)
sl = jk_audio.get_channel_by_slot(2)
sl.call()
# audio_codecs[0].channels[0].call()
# time.sleep(.1)
# audio_codecs[0].channels[0].get_hook_status()
# print(audio_codecs[0].channels[0].hook_status)
time.sleep(30)
sl.drop()
# audio_codecs[0].channels[0].drop()
# time.sleep(.5)
# print(audio_codecs[0].channels[0].hook_status)
