from twilio.twiml.voice_response import VoiceResponse, Say, Gather, Play

def initialCall(to, isLive, isDelayLive):
    if to == "+18445051150" and isLive == True: #If calling live number and is live
        response = VoiceResponse()
        gather = Gather(action="/gatherDigit", method="GET", num_digits=1, timeout=30)
        gather.play('http://twilio.willowcreek.org/mp3/LiveList.mp3')
        response.append(gather)
        return response
    elif to == "+18445051151" and isDelayLive == True: #If calling delayed number and is delay live
        response = VoiceResponse()
        gather = Gather(action="/gatherDigit", method="GET", num_digits=1, timeout=30)
        gather.play('http://twilio.willowcreek.org/mp3/DelayedList.mp3')
        response.append(gather)
        return response
    else:
        response = VoiceResponse()
        response.say('The language interpretation lines for the GLS are not yet open. Please call back 15 minutes prior to the next session')
        
        return response
