from twilio.rest import Client

from decouple import config
import os


phone_number = '+996557678010'
api_key = '7A620z5FTKab_CeziIuZhg=='
api_id = '4fe1c8015c3c465caba2bae852b55e81'
client = Client(api_key, api_id)

message = client.messages.create(
    body = 'Digitl Forge', from_='+12513095380', to=phone_number
)

'''


CURL CALL:
==========

curl "https://platform.clickatell.com/messages/http/send?apiKey=7A620z5FTKab_CeziIuZhg==&to=12345678&content=Test+message+text"





'''