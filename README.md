# Phoneboard
Phoneboard manages Twilio hosted conference calls and JK Audio AutoHybrid IP2 devices.


## Screenshots
|                    Desktop                     |                  Mobile                  |
|:----------------------------------------------:|:----------------------------------------:|
| ![phoneboard desktop](docs/img/phoneboard.png) | ![phoneboard mobile](docs/img/phone.png) |


## Controlling Phoneboard
![phoneboard control](docs/img/controls.png)

<kbd>l</kbd> brings up the main controls for phoneboard.  Groups of codecs and calls can be controlled with OFF-AIR, Queue, and ON-AIR.

* **OFF-AIR** - Set all channels to OFF-AIR.  This ends any existing codec calls and Twilio conferences.  Callers are instructed to redial 15 minutes before the conference.
* **Queue** - Opens up lines.  Callers are prompted for a room to join and placed on hold once the conference starts.
* **ON-AIR** - Set all channels to ON-AIR.  If disconnected, codecs will redial.

### Manual Controls
There are additional manual controls for phoneboard.  These are available for testing individual codec and Twilio API functions.  These can be accessed by pressing <kbd>e</kbd>.

<p align="center">
  <img height="300px" src="docs/img/manual_controls.png">
</p>

##### Watchdog Controls
* **Disabled** - Disables the watchdog for that channel. The codec is left in its current state.
* **OFF AIR** - Ends the Twilio conference via the Twilio API and drops the call on the codec.
* **ON AIR** - Dials the codec and redials once a call is dropped.

##### Codec Controls
* **call** - Set codec to dial.
* **drop** - set codec to drop call.

Clicking `codec` opens the codec management page. 

##### Twilio Controls
* **close** - Close conference via Twilio API.

## Keyboard Shortcuts
* <kbd>esc</kbd> - Reload
* <kbd>1</kbd>...<kbd>8</kbd> - Monitor conference channel
* <kbd>0</kbd> - End all WebRTC calls
* <kbd>c</kbd> - Toggle clocks
* <kbd>e</kbd> - Toggle manual controls
* <kbd>f</kbd> - Toggle fullscreen
* <kbd>l</kbd> - Toggle mastercontrol

## Call Monitoring
Using the Twilio WebRTC API, calls can be monitored within phoneboard.  Pressing <kbd>1</kbd>...<kbd>8</kbd> or clicking on the ON-AIR text will dial into the corresponding conference.  🎷 indicates a current WebRTC call.

On mobile devices, clicking **Live** and **Delay** dials the conference line for monitoring.

## Switchboard
Switchboard is a separate web server that serves TwiML for Twilio.  The Twilio service submits data to switchboard via a POST request.  TwiML supplied by Switchboard directs Twilio on how to route calls from the JK Audio codecs and phone calls to the DID numbers.

## Installation
Install git, python3-pip, and Node.js

```
$ sudo apt-get update
$ sudo apt-get install git python3-pip
$ curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
$ sudo apt-get install nodejs
```

Download phoneboard from github
```
$ git clone https://github.com/karlcswanson/phoneboard.git
$ cd phoneboard/
```

Install dependencies via npm & pip
```
$ npm install
$ pip3 install -r py/requirements.txt
```

build and run phoneboard
```
$ npm run build
$ npm run server
```
