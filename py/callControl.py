from twilio.twiml.voice_response import VoiceResponse, Say, Gather, Play, Dial
from re import match

import switchboard
import config

from status import conferenceStatus

#The languages are case sensitive
languages = {1: 'spanish', 2: 'chinese', 3: 'korean', 4: 'french'}
LANGUAGE_LIST = ['spanish', 'chinese', 'korean', 'french',
                 'spanishdelay', 'chinesedelay', 'koreandelay', 'frenchdelay']

# These paramaters come from the arguments within a GET request: To, Digits, From

STUDIO_LIGHT_MODES = ['on-air', 'off-air']

def group_is_closed():
    response = VoiceResponse()
    response.say(
        'The language interpretation lines for the GLS are not yet open. \
        Please call back 15 minutes prior to the next session'
    )
    return response


def initialCall(To, conference_name):
    if conference_name in LANGUAGE_LIST:

        if 'delay' in conference_name:
            group_status = conferenceStatus['delay']
        else:
            group_status = conferenceStatus['live']

        if group_status == 'off-air':
            return str(group_is_closed())



        response = VoiceResponse()
        dial = Dial()
        dial.conference(muted=True, beep=False, end_conference_on_exit=False,
                        start_conference_on_enter=False, max_participants=250,
                        trim="do-not-trim", wait_url="/conference/onHold",
                        wait_method="GET", name=conference_name)
        response.append(dial)

        return str(response)
    print('To: {}'.format(To))
    group = get_group_by_did(To)
    # print(group)
    if group:
        print(get_conference_status_by_group(group))
        if get_conference_status_by_group(group) == 'on-air':
            response = VoiceResponse()
            gather = Gather(action="/conference/gatherDigit", method="GET",
                            num_digits=1, timeout=30)
            gather.play(group['ivr_audio'])
            response.append(gather)
            return str(response)

    return str(group_is_closed())


def gatherDigits(To, digit):
    # If they pressed a correct option
    group = get_group_by_did(To)
    try:
        if group and digit in [1, 2, 3, 4]:
            mp3 = get_selected_language_mp3(group, digit)
            conference_name = get_conference_name(group, digit)

            # Build TWIML
            response = VoiceResponse()
            play = Play(mp3)
            response.append(play)
            dial = Dial()
            dial.conference(muted=True, beep=False, end_conference_on_exit=False,
                            start_conference_on_enter=False, max_participants=250,
                            trim="do-not-trim", wait_url="/conference/onHold",
                            wait_method="GET", name=conference_name)
            response.append(dial)
            return str(response)

    except KeyError:
        pass
    response = VoiceResponse()
    response.say("That is not a valid option")
    # this should take you back to the first URL and function initialCall
    response.redirect("/conference/join", method="GET")

    return str(response)

def conferenceOnHold():
    response = VoiceResponse()
    response.play("http://twilio.willowcreek.org/Hold.mp3", loop=0)
    return str(response)

def codecConference(From):
    conference_name = match("sip:(.*)@.*", From).group(1)

    if 'delay' in conference_name:
        group_status = conferenceStatus['delay']
    else:
        group_status = conferenceStatus['live']

    if group_status == 'off-air':
        return str(group_is_closed())

    response = VoiceResponse()
    dial = Dial()
    dial.conference(muted=False, beep=False, end_conference_on_exit=False,
                    start_conference_on_enter=True, max_participants=250,
                    trim="do-not-trim", name=conference_name)
    response.append(dial)

    return str(response)

def changeConferenceStatus(live, delay):
    if live in STUDIO_LIGHT_MODES:
        conferenceStatus['live'] = live

    if delay in STUDIO_LIGHT_MODES:
        conferenceStatus['delay'] = delay

def get_selected_language_mp3(group, digit):
    if group['title'] == 'Live Sites':
        return 'http://twilio.willowcreek.org/mp3/{}.mp3'.format(
            'live' + languages[digit])

    if group['title'] == 'Delay Sites':
        return 'http://twilio.willowcreek.org/mp3/{}.mp3'.format(
            'delayed' + languages[digit])

def get_conference_name(group, digit):
    if group['title'] == 'Live Sites':
        return languages[digit]

    if group['title'] == 'Delay Sites':
        return '{}delay'.format(languages[digit])


def get_conference_status_by_group(group):
    print(group['title'])
    print('get_conf by grop: {}'.format(conferenceStatus))
    if group['title'] == 'Live Sites':
        return conferenceStatus['live']

    if group['title'] == 'Delayed Sites':
        return conferenceStatus['delay']

    return 'off-air'

def get_group_by_did(did):
    for group in config.config_tree['groups']:
        if group['DID'] == did:
            return group
    return None
