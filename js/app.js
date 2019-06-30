"use strict";

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'whatwg-fetch';

import '../css/colors.scss';
import '../css/style.scss';
import '../node_modules/@ibm/plex/css/ibm-plex.css';

import { initLiveData } from './data.js';
import {  renderChannels } from './channelview.js';

export const phoneboard = [];
phoneboard.connectionStatus = 'CONNECTING'

$(document).ready(() => {
  renderChannels()
  initLiveData();




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
