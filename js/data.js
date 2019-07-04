
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

function checkReconnect() {
  fetch(dataURL)
    .then(response => response.json())
    .then((data) => {
      window.location.reload();
    }).catch((error) => {
      console.log(error);
    });
}

function wsConnect() {
  const loc = window.location;
  let newUri;

  if (loc.protocol === 'https:') {
    newUri = 'wss:';
  } else {
    newUri = 'ws:';
  }

  newUri += '//' + loc.host + loc.pathname + 'ws';

  phoneboard.socket = new WebSocket(newUri);

  phoneboard.socket.onmessage = (msg) => {
    const data = JSON.parse(msg.data);

    if (data['data-update']) {
      data['data-update'].forEach(updateSlot);
    }
  };

  phoneboard.socket.onclose = () => {
    ActivateMessageBoard();
  };

  phoneboard.socket.onerror = () => {
    ActivateMessageBoard();
  };
}

function ActivateMessageBoard() {
  $('#phoneboard').hide();
  $('.message-board').show();
  setInterval(checkReconnect, 1000);
}

function dataFilterFromList(data) {
  data.codecs.forEach((jk) => {
    jk.channels.forEach((ch) => {
      phoneboard.channels[ch.slot] = ch;
    });
  });
}

export function initLiveData(callback) {
  fetch(dataURL)
  .then(response => response.json())
  .then((data) => {
    data.codecs.forEach((jk) => {
      jk.channels.forEach((ch) => {
        console.log(ch);
        phoneboard.channels[ch.slot] = ch;
        // updateSlot(ch);
      });
    });
    callback();
  }).catch((error) => {
    console.log(error);
    phoneboard.connectionStatus = 'DISCONNECTED';
  });

  setTimeout(function() {
    console.log(phoneboard.channels)
  },200);

  // JsonUpdate();
  // setInterval(JsonUpdate, 500);
  wsConnect();
}
