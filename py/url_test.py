import config
from jk_audio import audio_codecs
import time

config.config()

print(audio_codecs[0].channels[0].hook_status)
audio_codecs[0].channels[0].call()
time.sleep(.1)
audio_codecs[0].channels[0].update_hook_status()
print(audio_codecs[0].channels[0].hook_status)
time.sleep(10)
audio_codecs[0].channels[0].drop()
time.sleep(.5)
print(audio_codecs[0].channels[0].hook_status)
