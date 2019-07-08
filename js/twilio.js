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

function startCall(id) {
  const channel = phoneboard.channels[id];
  const slotSelector = document.getElementById('slot-' + id);

  const deviceParams = {
    codecPreferences: ['opus', 'pcmu'],
  };

  const callParams = {
    language: generateConferenceName(channel.name),
  };

  console.log('starting call: ' + id);
  fetch('api/auth_token')
    .then(response => response.json())
    .then((data) => {
      const token = data.auth_token;
      channel.device = new Twilio.Device(token, deviceParams);
      channel.device.audio.outgoing(false);
      channel.device.audio.disconnect(false);

      channel.device.on('ready', (d) => {
        channel.connection = channel.device.connect(callParams);
      });

      channel.device.on('connect', (conn) => {
        setVolume(conn, slotSelector);
      });

      channel.device.on('error', (error) => {
        console.log(`Twilio.Device Error: ${  error.message}`);
      });

      channel.device.on('disconnect', (conn) => {
        channel.device.destroy();
        delete channel.device;
        endCall(slotSelector);
      });
    }).catch((error) => {
      console.log(error);
    });
}


function buttonClicked(id) {
  if (!phoneboard.channels[id].device) {
    startCall(id);
  }
  else {
    phoneboard.channels[id].connection.disconnect();
  }
}

export function activateTwiliowebRTC() {
  $('.studio-light').on('click', function (e) {
    const id = parseInt($(this).closest('.col-sm').attr('id').replace(/[^\d.]/g, ''));
    buttonClicked(id);
  });
}
