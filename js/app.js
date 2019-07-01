"use strict";

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'whatwg-fetch';
var moment = require('moment-timezone');


import '../css/colors.scss';
import '../css/style.scss';
import '../node_modules/@ibm/plex/css/ibm-plex.css';

import { initLiveData } from './data.js';
import {  renderChannels } from './channelview.js';

export const phoneboard = [];
phoneboard.connectionStatus = 'CONNECTING'



function updateClock(){
  let time = moment();
  document.querySelector('#et .time').innerHTML = time.tz("America/New_York").format('HH:mm:ss')
  document.querySelector('#ct .time').innerHTML = time.tz("America/Chicago").format('HH:mm:ss')
  document.querySelector('#mt .time').innerHTML = time.tz("America/Denver").format('HH:mm:ss')
  document.querySelector('#pt .time').innerHTML = time.tz("America/Los_Angeles").format('HH:mm:ss')
}


// https://developer.mozilla.org/en-US/docs/Web/API/Fullscreen_API
function toggleFullScreen() {
  if (!document.webkitFullscreenElement) {
    document.documentElement.webkitRequestFullscreen();
  } else if (document.webkitExitFullscreen) {
    document.webkitExitFullscreen();
  }
}


function toggleControls(){
  $('#phoneboard .col-sm .btn-group').toggle(400);
}

function toggleClockboard(){
  $('#clockboard').toggle(400);
}

function keybindings() {
  document.addEventListener('keydown', (e) => {
    if (e.keyCode === 27) {
      window.location.reload();
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



  }, false);
}





$(document).ready(() => {
  renderChannels()
  initLiveData();

  keybindings();
  toggleControls();

  setInterval(updateClock, 300);
  $('#phoneboard .col-sm .btn').on('click', function (e) {
    const id = $(this).closest('.col-sm').attr('id').replace(/[^\d.]/g, '');
    const cmd = $(this).val();

    console.log("cmd: " + cmd + " ID: " + id);

    let url = "/api/channel/" + id + "?cmd=" + cmd
    console.log(url);


    fetch(url, {
      method:'POST'
    }).then(/* ... */)
  });


});
