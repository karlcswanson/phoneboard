import { phoneboard } from './app.js';
import Twilio from 'twilio-client';

export function activateTwiliowebRTC() {
  $('.studio-light').on('click', function (e) {
    const id = parseInt($(this).closest('.col-sm').attr('id').replace(/[^\d.]/g, ''));
    buttonClicked(id);
  });
}

function buttonClicked(id){
  const slotSelector = document.getElementById('slot-' + id);

  if (!phoneboard.channels[id].device) {
    startCall(id);
  }
  else {
    console.log(phoneboard.channels[id].connection);
    phoneboard.channels[id].connection.disconnect();
  }
}

function startCall(id) {
  let channel = phoneboard.channels[id];

  const device_params = {
    codecPreferences: ['opus', 'pcmu']
  }

  const call_params = {
    language: generateConferenceName(channel.name)
  }

  console.log('starting call: ' + id);
  fetch('api/auth_token')
    .then(response => response.json())
    .then((data) => {
      const token = data.auth_token;
      channel.device = new Twilio.Device(token, device_params);
      channel.device.audio.outgoing(false);
      channel.device.audio.disconnect(false);

      const slotSelector = document.getElementById('slot-' + id);

      channel.device.on('ready', function(d){
        channel.connection = channel.device.connect(call_params);
      });

      channel.device.on('connect', function(conn) {
        setVolume(conn, slotSelector);
      });

      channel.device.on('disconnect', function(conn) {
        channel.device.destroy();
        delete channel.device;
        endCall(slotSelector);
      });



      console.log(channel.device);
    }).catch((error) => {
      console.log(error);
    });

}

function setVolume(connection, slotSelector) {
  slotSelector.querySelector('.webrtc-status').style.display = 'block';
  connection.on('volume', function(inputVolume, outputVolume){
    let width = outputVolume * 100.;
    width = width + '%';
    slotSelector.querySelector('.volume .progress-bar').style.width = width;
  });
}


function endCall(slotSelector) {
  slotSelector.querySelector('.volume .progress-bar').style.width = '0%';
  slotSelector.querySelector('.webrtc-status').style.display = 'none';
}

function generateConferenceName(name) {
  name = name.toLowerCase();
  name = name.replace(' live', '').replace(' delayed', 'delay');
  return name
}
