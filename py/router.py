from flask import Flask, Response, request
import callControl

app = Flask(__name__)

# print(callControl.initialCall(To="+18445051150",isLive=True,isDelayLive=True))

@app.route('/conference/join')
def join():
    To = request.args.get('To')
    print(To)
    return Response(callControl.initialCall(To=To), mimetype='text/xml')

@app.route('/conference/gatherDigit')
def gatherDigit():
    To = request.args.get('To')
    Digit = request.args.get('Digit')
    return Response(callControl.gatherDigits(To=To,Digit=Digit), mimetype='text/xml')

@app.route('/conference/onHold')
def onHold():
    return Response(callControl.conferenceOnHold(), mimetype='text/xml')

@app.route('/conference/codecs')
def codecs():
    From = request.args.get('From')
    return Response(callControl.codecConference(From=From), mimetype='text/xml')

if __name__ == '__main__':
    app.run()