import { phoneboard } from './app.js';
import Twilio from 'twilio-client';


function generateConferenceName(name) {
  name = name.toLowerCase();
  name = name.replace(' live', '').replace(' delayed', 'delay');
  return name
}


function setVolume(connection, slotSelector) {
  slotSelector.querySelector('.webrtc-status').style.display = 'block';
  connection.on('volume', (inputVolume, outputVolume) => {
    const width = `${Math.floor(outputVolume * 100)}%`;
    // console.log("width: " + width);
    slotSelector.querySelector('.volume .progress-bar').style.width = width;
  });
}

function endCall(slotSelector) {
  slotSelector.querySelector('.volume .progress-bar').style.width = '0%';
  slotSelector.querySelector('.webrtc-status').style.display = 'none';
}

export function endOtherCalls(id) {
  phoneboard.channels.forEach((ch) => {
    if (ch.slot !== id) {
      if (ch.connection) {
        ch.connection.disconnect();
      }
    }
  });
}

function startCall(id) {
  // let channel = phoneboard.channels[id];
  const slotSelector = document.getElementById('slot-' + id);

  const deviceParams = {
    codecPreferences: ['opus', 'pcmu'],
  };

  const callParams = {
    language: generateConferenceName(phoneboard.channels[id].name),
  };

  console.log('starting call: ' + id);
  fetch('api/auth_token')
    .then(response => response.json())
    .then((data) => {
      const token = data.auth_token;
      phoneboard.channels[id].device = new Twilio.Device(token, deviceParams);
      phoneboard.channels[id].device.audio.outgoing(false);
      phoneboard.channels[id].device.audio.disconnect(false);

      phoneboard.channels[id].device.on('ready', (device) => {
        phoneboard.channels[id].connection = device.connect(callParams);
      });

      phoneboard.channels[id].device.on('connect', (conn) => {
        console.log(phoneboard.channels[id]);
        // endOtherCalls(id);
        setVolume(conn, slotSelector);
      });

      phoneboard.channels[id].device.on('error', (error) => {
        console.log(`Twilio.Device Error: ${error.message}`);
      });

      phoneboard.channels[id].device.on('disconnect', (conn) => {
        phoneboard.channels[id].device.destroy();
        delete phoneboard.channels[id].device;
        endCall(slotSelector);
      });
    }).catch((error) => {
      console.log(error);
    });
}




export function buttonClicked(id) {
  endOtherCalls(id);
  if (!phoneboard.channels[id].device) {
    startCall(id);
  } else {
    phoneboard.channels[id].connection.disconnect();
  }
}

export function activateTwiliowebRTC() {
  $('.studio-light').on('click', function (e) {
    const id = parseInt($(this).closest('.col-sm').attr('id').replace(/[^\d.]/g, ''));
    buttonClicked(id);
  });
}
