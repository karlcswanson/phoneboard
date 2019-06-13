from twilio.rest import Client

import config



config.config()

account_sid = config.config_tree['twilio']['account_sid']
auth_token = config.config_tree['twilio']['auth_token']
client = Client(account_sid, auth_token)

conferences = client.conferences.list(limit=20)

for conference in conferences:
    if conference.status in ['init', 'in-progress']:
        participants = conference.participants.list()
        participant_count = len(participants) - 1
        print('Conference: {} on call: {}'.format(conference.friendly_name, participant_count))
