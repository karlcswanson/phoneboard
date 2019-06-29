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
});
