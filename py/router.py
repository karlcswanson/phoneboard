from flask import Flask, Response, request
import callControl

app = Flask(__name__)

# print(callControl.initialCall(To="+18445051150",isLive=True,isDelayLive=True))

@app.route('/conference/join')
def join():
    To = request.args.get('To')
    return Response(callControl.initialCall(To=To), mimetype='text/xml')

@app.route('/conference/gatherDigit')
def gatherDigits():
    To = request.args.get('To')
    Digits = int(request.args.get('Digits'))
    return Response(callControl.gatherDigits(To=To,Digits=Digits), mimetype='text/xml')

@app.route('/conference/onHold')
def onHold():
    return Response(callControl.conferenceOnHold(), mimetype='text/xml')

@app.route('/conference/codecs')
def codecs():
    From = request.args.get('From')
    return Response(callControl.codecConference(From=From), mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug=True)