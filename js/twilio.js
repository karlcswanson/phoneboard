import { phoneboard } from './app.js';
import Twilio from 'twilio-client';

export function activateTwiliowebRTC() {
  $('.studio-light').on('click', function (e) {
    const id = parseInt($(this).closest('.col-sm').attr('id').replace(/[^\d.]/g, ''));

    if (!phoneboard.channels[id].device) {
      startCall(id);
    }
    else {
      endCall(id);
    }
  });
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
        channel.device.connect(call_params);
      });

      channel.device.on('connect', function(conn){
        setVolume(conn, slotSelector);
      });

      channel.device.on('disconnect', function(conn){
        endCall(id);
      });



      console.log(channel.device);
    }).catch((error) => {
      console.log(error);
    });

}

function setVolume(connection, slotSelector) {
  connection.on('volume', function(inputVolume, outputVolume){
    let width = outputVolume * 100.;
    width = width + '%';
    slotSelector.querySelector('.volume .progress-bar').style.width = width;
  });
}


function endCall(id) {
  let channel = phoneboard.channels[id];
  channel.device.disconnectAll();
  channel.device.destroy();
  delete channel.device;

  const slotSelector = document.getElementById('slot-' + id);
  slotSelector.querySelector('.volume .progress-bar').style.width = '0%';
}

function generateConferenceName(name) {
  name = name.toLowerCase();
  name = name.replace(' live', '').replace(' delayed', 'delay');
  return name
}
