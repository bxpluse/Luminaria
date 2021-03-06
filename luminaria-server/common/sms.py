from enum import Enum

from twilio.rest import Client

from common.logger import log, LogLevel
from database.config.global_config_model import GlobalConfigModel

TWILIO_SID = GlobalConfigModel.retrieve('TWILIO_SID')
TWILIO_TOKEN = GlobalConfigModel.retrieve('TWILIO_TOKEN')
TWILIO_FROM_NUMBER = GlobalConfigModel.retrieve('TWILIO_FROM_NUMBER')
TWILIO_TO_NUMBER = GlobalConfigModel.retrieve('TWILIO_TO_NUMBER')


class When(Enum):
    DUMMY = 0
    NOW = 1


def send(msg, requester=None, when=When.NOW):
    log_message = ''
    if requester:
        log_message += '(Requester: {0})'.format(requester)
    log_message += ' ' + msg

    try:
        if when == When.NOW:
            send_sms(msg)
        log(app_name='sms', message=log_message)
    except Exception as exception:
        msg_with_error = 'FAILED TO SEND SMS EXCEPTION: {0} | {1} '.format(str(exception), log_message)
        log(app_name='sms', message=msg_with_error, level=LogLevel.ERROR)


def send_sms(msg):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(to=TWILIO_TO_NUMBER, from_=TWILIO_FROM_NUMBER, body=msg)
