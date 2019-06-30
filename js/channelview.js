import { phoneboard } from './app.js'


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
}

export function updateSlot(data) {
  if (data.slot === 0) {
    return;
  }
  const slot = 'slot-' + data.slot;
  const slotSelector = document.getElementById(slot);
  if (slotSelector) {
    updateViewOnly(slotSelector, data);
  }
}

export function renderChannels(){
  // TODO FIX THIS!
  for(let i = 1; i <= 4; i++) {
    let t;
    t = document.getElementById('channel-template').content.cloneNode(true);
    t.querySelector('div.col-sm').id = 'slot-' + i;
    document.getElementById('live-row').appendChild(t);
  }

  for(let i = 5; i <= 8; i++) {
    let t;
    t = document.getElementById('channel-template').content.cloneNode(true);
    t.querySelector('div.col-sm').id = 'slot-' + i;
    document.getElementById('delay-row').appendChild(t);
  }


}
