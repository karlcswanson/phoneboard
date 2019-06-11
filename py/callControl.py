from twilio.twiml.voice_response import VoiceResponse, Say, Gather, Play, Dial

languages = {1: "Spanish", 2: "Chinese", 3: "Korean", 4: "French"} #We should move this to the config file

#These paramaters come from the arguments within a GET request: To, Digits

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

def gatherDigits(to,digit):
    #If they pressed a correct option
    try:
        #This if statement generates the MP3 announement file on the fly so we can avoid having to build a seperate dictionary
        if to == "+18445051150": #These numbers need to be moved to the config file
            mp3 = "http://twilio.willowcreek.org/mp3/{}.mp3".format("Live" + languages[digit])
        else:
            mp3 = "http://twilio.willowcreek.org/mp3/{}.mp3".format("Delayed" + languages[digit])
        #This will generate the wait URL
        if to == "+18445051150":
            waitUrl = "http://twilio.willowcreek.org/wait/{}".format(languages[digit]).lower() #This URL will be different
        else:
            waitUrl = "http://twilio.willowcreek.org/wait/{}delay".format(languages[digit]).lower() #This URL will be different
        # And finally the conference name
        if to == "+18445051150":
            conferenceName = languages[digit]
        else:
            conferenceName = "{}delay".format(languages[digit])

        #Build TWIML
        response = VoiceResponse()
        play = Play(mp3)
        response.append(play)
        dial = Dial()
        dial.conference(muted=True, beep=False, end_conference_on_exit=False, start_conference_on_enter=False, max_participants=250, trim="do_not_trim", wait_url=waitUrl, name=conferenceName)
        response.append(dial)

        return response
    except KeyError:
        pass
        response = VoiceResponse()
        response.say("That is not a valid option")
        response.redirect("/hello") #this should take you back to the first URL and function initialCall

        return response


print(gatherDigits("+18445051151", 6))