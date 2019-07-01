
import { phoneboard } from './app.js';
import { updateSlot } from './channelview.js';

let dataURL = 'data'

function JsonUpdate() {
  fetch(dataURL)
    .then(response => response.json())
    .then((data) => {
      if (phoneboard.connectionStatus === 'DISCONNECTED') {
        // window.location.reload();
      }
      data.codecs.forEach((codec) => {
        codec.channels.forEach(updateSlot);
      });
      phoneboard.connectionStatus = 'CONNECTED';
      phoneboard.config = data.config;
    }).catch((error) => {
      console.log(error);
      phoneboard.connectionStatus = 'DISCONNECTED';
    });
}

export function initLiveData() {
  JsonUpdate();
  // setInterval(JsonUpdate, 1000);
}
