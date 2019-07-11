"use strict";

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'whatwg-fetch';
import Twilio from 'twilio-client';
var moment = require('moment-timezone');

import '../css/colors.scss';
import '../css/live.scss';
import '../node_modules/@ibm/plex/css/ibm-plex.css';


let TwilioDevice;
let TwilioConnection;


function randomNumber() {
  return Math.floor(Math.random() * 100);
}

function endCall() {
  document.getElementById('vu').style.width = '0%';
  $('#end').hide();
  $('#listen').show();
}

function setVolume(connection) {
  connection.on('volume', (inputVolume, outputVolume) => {
    const height = `${Math.floor(outputVolume * 100)}%`;
    // console.log("height: " + height);
    document.querySelector('.v-progress-bar').style.height = height;
  });
}


function startCall(voiceChannel) {
  const deviceParams = {
    codecPreferences: ['opus', 'pcmu'],
  };

  const callParams = {
    language: voiceChannel,
  };

  console.log('starting call: ' + voiceChannel);
  fetch('../api/auth_token')
    .then(response => response.json())
    .then((data) => {
      const token = data.auth_token;
      TwilioDevice = new Twilio.Device(token, deviceParams);
      // TwilioDevice.audio.outgoing(false);
      // TwilioDevice.audio.disconnect(false);

      TwilioDevice.on('ready', (device) => {
        TwilioConnection = device.connect(callParams);
      });

      TwilioDevice.on('connect', (conn) => {
        $('#listen').hide();
        $('#end').show();
        setVolume(conn);
      });

      TwilioDevice.on('error', (error) => {
        console.log(`Twilio.Device Error: ${error.message}`);
      });

      TwilioDevice.on('disconnect', (conn) => {
        TwilioDevice.destroy();
        // delete TwilioDevice;
        endCall();
      });
    }).catch((error) => {
      console.log(error);
    });
}


function randomVU() {
  const rand = randomNumber();
  // console.log('random: '+ rand);
  document.getElementById('vu').style.height = `${rand}%`;
}



function initWebRTC() {
  $('#listen').on('click', () => {
    const channel = $('#chooser :selected').val();
    startCall(channel);
  });

  $('#end').on('click', () => {
    TwilioConnection.disconnect();
  });
}

$(document).ready(() => {
  $('#end').hide();
  // setInterval(randomVU, 100);
  initWebRTC();
  console.log('hello!');
});
