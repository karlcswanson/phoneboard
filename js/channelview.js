import { phoneboard } from './app.js';
import { activateTwiliowebRTC } from './twilio.js';

function updateName(slotSelector, data) {
  slotSelector.querySelector('p.name').innerHTML = data.name;
}

function updateStatus(slotSelector, data){
  slotSelector.querySelector('div.channel_name').className = 'channel_name';
  slotSelector.querySelector('div.channel_name').classList.add(data.status);
}

function updateCodecStatus(slotSelector, data){
  slotSelector.querySelector('p.codec-status').className = 'codec-status';
  slotSelector.querySelector('p.codec-status').classList.add(data.codec_status);
}

function updateCodecTime(slotSelector, data){
  slotSelector.querySelector('p.codec-time').innerHTML = data.call_time;
}

function updateCodecDrop(slotSelector, data){
  slotSelector.querySelector('p.codec-drop').innerHTML = '';
}

function updateConferenceStatus(slotSelector, data){
  slotSelector.querySelector('p.conference-status').className = 'conference-status';
  slotSelector.querySelector('p.conference-status').classList.add(data.conf_status);
}

function updateConferenceTime(slotSelector, data){
  slotSelector.querySelector('p.conference-time').innerHTML = data.conf_time;
}

function updateConferenceSize(slotSelector, data){
  slotSelector.querySelector('p.conference-size span').innerHTML = data.conf_count;
}

function updateStudioLight(slotSelector, data){
  slotSelector.querySelector('p.studio-light').innerHTML = data.studio_light.replace('-', ' ');
  slotSelector.querySelector('p.studio-light').className = 'studio-light';
  slotSelector.querySelector('p.studio-light').classList.add(data.studio_light);
}

function updateIP(slotSelector, data){
  slotSelector.querySelector('p.codec-status a').href = 'http://' + data.ip;
}

function updateDrops(slotSelector, data){
  slotSelector.querySelector('p.codec-drop span').innerHTML = data.drops;
}

function updateViewOnly(slotSelector, data) {
  if('name' in data){
    updateName(slotSelector, data);
  }
  if('status' in data){
    updateStatus(slotSelector, data);
  }
  if('codec_status' in data){
    updateCodecStatus(slotSelector, data);
  }
  if('call_time' in data){
    updateCodecTime(slotSelector, data);
  }
  if('conf_status' in data){
    updateConferenceStatus(slotSelector, data);
  }
  if('conf_time' in data){
    updateConferenceTime(slotSelector, data);
  }
  if('conf_count' in data){
    updateConferenceSize(slotSelector, data);
  }
  if('studio_light' in data){
    updateStudioLight(slotSelector, data);
  }
  if('ip' in data){
    updateIP(slotSelector, data);
  }
  if('drops' in data){
    updateDrops(slotSelector, data);
  }
}

function updateCheck(data, key, callback) {
  if (key in data) {
    if (phoneboard.channels[data.slot][key] !== data[key]) {
      if (callback) {
        callback();
      }
      phoneboard.channels[data.slot][key] = data[key];
    }
  }
}

function updateSelector(slotSelector, data) {
  updateCheck(data, 'name', () => {
    updateName(slotSelector, data);
  });
  updateCheck(data, 'status', () => {
    updateStatus(slotSelector, data);
  });
  updateCheck(data, 'codec_status', () => {
    updateCodecStatus(slotSelector, data);
  });
  updateCheck(data, 'call_time', () => {
    updateCodecTime(slotSelector, data);
  });
  updateCheck(data, 'conf_status', () => {
    updateConferenceStatus(slotSelector, data);
  });
  updateCheck(data, 'conf_time', () => {
    updateConferenceTime(slotSelector, data);
  });
  updateCheck(data, 'conf_count', () => {
    updateConferenceSize(slotSelector, data);
  });
  updateCheck(data, 'studio_light', () => {
    updateStudioLight(slotSelector, data);
  });
  updateCheck(data, 'ip', () => {
    updateIP(slotSelector, data);
  });
  updateCheck(data, 'drops', () => {
    updateDrops(slotSelector, data);
  });
}


export function updateSlot(data) {
  if (data.slot === 0) {
    return;
  }
  const slot = 'slot-' + data.slot;
  const slotSelector = document.getElementById(slot);
  if (slotSelector) {
    updateSelector(slotSelector, data);
  }
}


function buttonSetup() {
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

  $('#mastercontrol .col-sm .btn').on('click', function (e) {
    const id = $(this).closest('.col-sm').attr('id').replace(/[^\d.]/g, '');
    const cmd = $(this).val();

    console.log("cmd: " + cmd + " ID: " + id);

    let url = "/api/group/" + id + "?cmd=" + cmd
    console.log(url);


    fetch(url, {
      method:'POST'
    }).then(/* ... */)
  });
}


function infoToggle() {
  $('.channel_name').on('click', function (e) {
    const id = $(this).closest('.col-sm').attr('id');
    if ($(window).width() <= 512) {
      $('#' + id + ' .info-drawer').toggle();
      $('#' + id + ' .studio-light-box').toggle();
    }
  });
}



export function renderChannels(){
  // TODO Match from group config file
  for(let i = 1; i <= 4; i++) {
    let t;
    t = document.getElementById('channel-template').content.cloneNode(true);
    t.querySelector('div.col-sm').id = 'slot-' + i;
    console.log(phoneboard.channels[i]);
    updateViewOnly(t, phoneboard.channels[i]);
    document.getElementById('live-row').appendChild(t);
  }


  for(let i = 5; i <= 8; i++) {
    let t;
    t = document.getElementById('channel-template').content.cloneNode(true);
    t.querySelector('div.col-sm').id = 'slot-' + i;
    updateViewOnly(t, phoneboard.channels[i]);
    document.getElementById('delay-row').appendChild(t);
  }
  $('#phoneboard .col-sm .btn-group').toggle();
  $('#mastercontrol').toggle();
  buttonSetup();
  infoToggle();
  activateTwiliowebRTC();
}
