import time
from datetime import datetime
import logging

from twilio.rest import Client
from twilio.rest.api.v2010.account.conference import ConferenceInstance
from twilio.jwt.client import ClientCapabilityToken

import config

TWILIO_TIMEOUT = 30

conn = []

conference_list = []




class TwilioConnection:
    def __init__(self):
        self.timestamp = time.time() - 60
        account_sid = config.config_tree['twilio']['account_sid']
        auth_token = config.config_tree['twilio']['auth_token']

        self.client = Client(account_sid, auth_token)


    def active_conferences(self):
        active_conference_list = []

        for conference in self.client.conferences.list(limit=20):
            if conference.status in ['init', 'in-progress']:
                active_conference_list.append(conference)

        self.timestamp = time.time()
        return active_conference_list

    def is_connected(self):
        if (time.time() - self.timestamp) < TWILIO_TIMEOUT:
            return True
        return False


class ConferenceRoom:
    def __init__(self, conference):
        self.conference = conference
        participants = conference.participants.list()

        self.codec_status = 'OPEN'
        for p in participants:
            if p.muted == False:
                self.codec_status = 'CONNECTED'

        if self.codec_status == 'CONNECTED':
            self.call_count = len(participants) - 1
        else:
            self.call_count = len(participants)


        self.call_start = datetime.timestamp(conference.date_created)
        self.name = conference.friendly_name
        self.timestamp = time.time()


    def call_time(self):
        delta = time.time() - self.call_start
        return time.strftime('%H:%M:%S', time.gmtime(delta))

    def close_room(self):
        try:
            self.conference.update(status='completed')
        except:
            logging.debug("unable to close room")

    def status(self):
        if (time.time() - self.timestamp) < TWILIO_TIMEOUT:
            return self.codec_status
        return 'UNKNOWN'

    def conference_json(self):
        return {
            'name': self.name, 'status': self.status(),
            'call_count': self.call_count, 'call_time': self.call_time()
        }


def twilio_query_service():
    while True:
        global conference_list
        c_list = []
        try:
            conferences = conn.active_conferences()
            for conference in conferences:
                c_list.append(ConferenceRoom(conference))


        except:
            logging.warning('Unable to update conferences')

        conference_list = c_list
        time.sleep(5)


def get_conference_by_name(name):
    name = name.replace(' ', '').lower()
    name = name.replace('live', '').replace('delayed', 'delay')
    for conference in conference_list:
        if conference.name == name:
            return conference
    return None

def get_capability_token():
    account_sid = config.config_tree['twilio']['account_sid']
    auth_token = config.config_tree['twilio']['auth_token']
    application_sid = config.config_tree['twilio']['webrtc_sid']

    capability = ClientCapabilityToken(account_sid, auth_token)
    capability.allow_client_outgoing(application_sid)
    token = capability.to_jwt()
    return token.decode("utf-8")



def twilio_setup():
    global conn
    conn = TwilioConnection()

def main():
    config.config()
    twilio_setup()
    twilio_query_service()


if __name__ == '__main__':
    main()
