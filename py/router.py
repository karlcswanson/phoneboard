from flask import Flask, Response
import callControl

app = Flask(__name__)

# print(callControl.initialCall(To="+18445051150",isLive=True,isDelayLive=True))

@app.route('/conference/join')
def join():
    return Response(callControl.initialCall(To="+18445051150"), mimetype='text/xml')

@app.route('/conference/gatherDigit')
def gatherDigit():
    return Response(callControl.gatherDigits(To="+18445051150",Digit=6), mimetype='text/xml')

@app.route('/conference/onHold')
def onHold():
    return Response(callControl.conferenceOnHold(), mimetype='text/xml')


if __name__ == '__main__':
    app.run(debug = True)