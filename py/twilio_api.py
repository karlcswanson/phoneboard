import time
from datetime import datetime

from twilio.rest import Client
from twilio.rest.api.v2010.account.conference import ConferenceInstance

import config

TWILIO_TIMEOUT = 10

conn = []

conference_list = []


class TwilioConnection:
    def __init__(self):
        account_sid = config.config_tree['twilio']['account_sid']
        auth_token = config.config_tree['twilio']['auth_token']

        self.client = Client(account_sid, auth_token)

    def active_conferences(self):
        active_conference_list = []

        for conference in self.client.conferences.list(limit=20):
            if conference.status in ['init', 'in-progress']:
                active_conference_list.append(conference)

        return active_conference_list


class ConferenceRoom:
    def __init__(self, conference):
        self.conference = conference
        participants = conference.participants.list()

        self.codec_status = 'DISCONNECTED'
        for p in participants:
            if p.muted == False:
                self.codec_status = 'CONNECTED'
                self.call_count = len(participants) - 1

        if self.codec_status == 'CONNECTED':
            self.call_count = len(participants) - 1
        else:
            self.call_count = len(participants)


        self.call_start = datetime.timestamp(conference.date_created)
        self.name = conference.friendly_name
        self.timestamp = time.time()


    def call_time(self):
        if self.codec_status == 'CONNECTED':
            delta = time.time() - self.call_start
            return time.strftime('%H:%M:%S', time.gmtime(delta))

        return '--:--:--'

    def close_room(self):
        self.conference.update(status='completed')

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
        conference_list = []
        conferences = conn.active_conferences()
        for conference in conferences:
            conference_list.append(ConferenceRoom(conference))


        for c in conference_list:
            print(c.conference_json())

        time.sleep(5)


def twilio_setup():
    global conn
    conn = TwilioConnection()

def main():
    config.config()
    twilio_setup()

    twilio_query_service()




if __name__ == '__main__':
    main()
