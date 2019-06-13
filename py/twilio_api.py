

from twilio.rest import Client
from twilio.rest.api.v2010.account.conference import ConferenceInstance

import config


class TwilioConnection:
    def __init__(self):
        account_sid = config.config_tree['twilio']['account_sid']
        auth_token = config.config_tree['twilio']['auth_token']

        self.client = Client(account_sid, auth_token)

    def open_conferences(self):
        conference_list = []

        for conference in self.client.conferences.list(limit=20):
            if conference.status in ['init', 'in-progress']:
                conference_list.append(conference)

        return conference_list




# ConferenceInstance methods
def close(self):
    self.update(status = 'completed')

def call_count(self):
    return len(self.participants.list())

def codec_in_conference(self):
    for p in self.participants.list():
        if p.muted == False:
            return True
    return False





def main():
    ConferenceInstance.close = close
    ConferenceInstance.call_count = call_count
    ConferenceInstance.codec_in_conference = codec_in_conference


    config.config()
    conn = TwilioConnection()

    conferences = conn.open_conferences()

    for i in conferences:
        print('Conference: {}, participants {}'.format(i.friendly_name, i.call_count()))
        if i.codec_in_conference():
            print('Codec Is Live')
            # i.close()
        else:
            print('Codec Is off')




if __name__ == '__main__':
    main()
