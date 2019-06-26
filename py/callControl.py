from twilio.twiml.voice_response import VoiceResponse, Say, Gather, Play, Dial
from re import match
from config import is_delay_live,is_live

languages = {1: "Spanish", 2: "Chinese", 3: "Korean",
             4: "French"}  # We should move this to the config file

# These paramaters come from the arguments within a GET request: To, Digits, From

def initialCall(To):
    if To == "+18445051150" and is_live():  # If calling live number and is live
        response = VoiceResponse()
        gather = Gather(action="/conference/gatherDigit", method="GET",
                        num_digits=1, timeout=30)
        gather.play('http://twilio.willowcreek.org/mp3/LiveList.mp3')
        response.append(gather)
        return str(response)
    elif To == "+18445051151" and is_delay_live():  # If calling delayed number and is delay live
        response = VoiceResponse()
        gather = Gather(action="/conference/gatherDigit", method="GET",
                        num_digits=1, timeout=30)
        gather.play('http://twilio.willowcreek.org/mp3/DelayedList.mp3')
        response.append(gather)
        return str(response)
    else:
        response = VoiceResponse()
        response.say(
            'The language interpretation lines for the GLS are not yet open. \
            Please call back 15 minutes prior to the next session')

        return str(response)


def gatherDigits(To, Digits):
    # If they pressed a correct option
    try:
        # This if statement generates the MP3 announement file on the fly so we can avoid having to build a seperate dictionary
        if To == "+18445051150":  # These numbers need to be moved to the config file
            mp3 = "http://twilio.willowcreek.org/mp3/{}.mp3".format(
                "Live" + languages[Digits])
        else:
            mp3 = "http://twilio.willowcreek.org/mp3/{}.mp3".format(
                "Delayed" + languages[Digits])
        # This will generate the wait URL, the function is conferenceOnHold
        # After looking at this, I dont think we need it actually...
        if To == "+18445051150":
            # This URL will be different
            waitUrl = "http://twilio.willowcreek.org/wait/{}".format(
                languages[Digits]).lower()
        else:
            # This URL will be different
            waitUrl = "http://twilio.willowcreek.org/wait/{}delay".format(
                languages[Digits]).lower()
        # And finally the conference name
        if To == "+18445051150":
            conferenceName = languages[Digits]
        else:
            conferenceName = "{}delay".format(languages[Digits])

        # Build TWIML
        response = VoiceResponse()
        play = Play(mp3)
        response.append(play)
        dial = Dial()
        dial.conference(muted=True, beep=False, end_conference_on_exit=False, start_conference_on_enter=False,
                        max_participants=250, trim="do_not_trim", wait_url=waitUrl, name=conferenceName)
        response.append(dial)

        return str(response)
    except KeyError:
        pass
        response = VoiceResponse()
        response.say("That is not a valid option")
        # this should take you back to the first URL and function initialCall
        response.redirect("/conference/join",method="GET")

        return str(response)

def conferenceOnHold():
    response = VoiceResponse()
    response.play("http://twilio.willowcreek.org/Hold.mp3", loop=0)
    return str(response)


def codecConference(From):
    conferenceName = match("sip:(.*)@.*", From).group(1)

    response = VoiceResponse()
    dial = Dial()
    dial.conference(muted=False, beep=False, end_conference_on_exit=False,
                    start_conference_on_enter=True, max_participants=250, trim="do_not_trim", name=conferenceName)
    response.append(dial)

    return str(response)