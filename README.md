# Phoneboard
Phoneboard manages Twilio hosted conference calls and JK Audio AutoHybrid IP2 devices.


## Screenshots
![phoneboard desktop](docs/img/phoneboard.png)
![phoneboard mobile](docs/img/phone.png)


## Keyboard Shortcuts
* <kbd>esc</kbd> - Reload
* <kbd>1</kbd> - <kbd>8</kbd> - Monitor conference channel
* <kbd>c</kbd> - Toggle clocks
* <kbd>e</kbd> - Toggle manual controls
* <kbd>f</kbd> - Toggle fullscreen
* <kbd>l</kbd> - Toggle mastercontrol

## Installation
Download phoneboard from github
```
git clone https://github.com/karlcswanson/phoneboard.git
cd phoneboard/
```

Install dependencies via npm & pip
```
npm install
pip3 install -r py/requirements.txt
```

build and run phoneboard
```
npm run build
npm run server
```
