"use strict";

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'whatwg-fetch';
var moment = require('moment-timezone');


import '../css/colors.scss';
import '../css/style.scss';
import '../node_modules/@ibm/plex/css/ibm-plex.css';

import { initLiveData } from './data.js';
import { renderChannels } from './channelview.js';
import { buttonClicked, endOtherCalls } from './twilio.js';

export const phoneboard = [];
phoneboard.connectionStatus = 'CONNECTING'
phoneboard.channels = [];


function updateClock() {
  const time = moment();
  document.querySelector('#et .time').innerHTML = time.tz('America/New_York').format('hh:mm:ss');
  document.querySelector('#ct .time').innerHTML = time.tz('America/Chicago').format('hh:mm:ss');
  document.querySelector('#mt .time').innerHTML = time.tz('America/Denver').format('hh:mm:ss');
  document.querySelector('#pt .time').innerHTML = time.tz('America/Los_Angeles').format('hh:mm:ss');
}


// https://developer.mozilla.org/en-US/docs/Web/API/Fullscreen_API
function toggleFullScreen() {
  if (!document.webkitFullscreenElement) {
    document.documentElement.webkitRequestFullscreen();
  } else if (document.webkitExitFullscreen) {
    document.webkitExitFullscreen();
  }
}


function toggleControls() {
  $('.btn-test-group').toggle(400);
}

function toggleClockboard() {
  $('#clockboard').toggle(400);
}

function toggleMastercontrol() {
  $('#mastercontrol').toggle(400);
}


function keybindings() {
  document.addEventListener('keydown', (e) => {
    if (e.keyCode === 27) {
      window.location.reload();
    }

    if (e.keyCode === 48) {
      endOtherCalls(0);
    }
    if (e.keyCode === 49) {
      buttonClicked(1);
    }
    if (e.keyCode === 50) {
      buttonClicked(2);
    }
    if (e.keyCode === 51) {
      buttonClicked(3);
    }
    if (e.keyCode === 52) {
      buttonClicked(4);
    }
    if (e.keyCode === 53) {
      buttonClicked(5);
    }
    if (e.keyCode === 54) {
      buttonClicked(6);
    }
    if (e.keyCode === 55) {
      buttonClicked(7);
    }
    if (e.keyCode === 56) {
      buttonClicked(8);
    }


    if (e.keyCode === 67) {
      toggleClockboard();
    }

    if (e.keyCode === 69) {
      toggleControls();
    }

    if (e.keyCode === 70) {
      toggleFullScreen();
    }

    if (e.keyCode === 76) {
      toggleMastercontrol();
    }
  }, false);
}


$(document).ready(() => {
  initLiveData(renderChannels);

  keybindings();

  setInterval(updateClock, 300);
});
