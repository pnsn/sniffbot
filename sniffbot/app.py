'''
Where all the magic happens again, and again and again
'''
from flask import request, Flask
from .config import app_config
from .models import SniffWave
from twilio.twiml.messaging_response import (
    MessagingResponse,
    Message,
    Body
)
import re

MAX_SECONDS = 5
DEFAULT_SECONDS = 3


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    EWORM_HOST_PRODUCTION = app.config['EWORM_HOST_PRODUCTION']
    EWORM_HOST_STAGING = app.config['EWORM_HOST_STAGING']
    EWORM_USER = app.config['EWORM_USER']
    EWORM_RING = app.config['EWORM_RING']
    SSH_I_FILE = app.config['SSH_I_FILE']

    def get_sniffwave(host):
        '''http route for staging and production '''
        sta = sanitize_scnl(request.args.get('sta'), 3, 5, 'HTTP')
        if len(request.args) < 1 or sta is None:
            return help_message_http()
        chan = sanitize_scnl(request.args.get('chan'), 3, 3, 'HTTP')
        net = sanitize_scnl(request.args.get('net'), 2, 2, 'HTTP')
        sec = request.args.get('sec')
        if sec is not None:
            try:
                sec = min(int(sec), MAX_SECONDS)
                sec = sanitize_sec(sec, 'HTTP')
            except ValueError:
                sec = DEFAULT_SECONDS
        sn = SniffWave(host, EWORM_USER, EWORM_RING,
                       SSH_I_FILE, sta, chan, net, sec)
        stdout = sn.call()
        print(stdout.split('\n'))
        return stdout

    def post_sniffwave(host):
        '''route for sms for staging and production'''
        body = request.form['Body']
        query = body.split()
        if not query:
            return help_message_sms()
        try:
            sta, sec = query
        except ValueError:
            sec = str(DEFAULT_SECONDS)
        sta = sanitize_scnl(query[0].upper(), 3, 5, "SMS")
        if sec is not None:
            try:
                sec = min(int(sec), MAX_SECONDS)
                sec = sanitize_sec(sec, "SMS")
            except ValueError:
                sec = DEFAULT_SECONDS
        sn = SniffWave(host, EWORM_USER, EWORM_RING,
                       SSH_I_FILE, sta, None, None, sec)
        stdout = sn.call()
        msg = sn.format_sms_response(stdout)
        return create_sms(msg)

    def sanitize_scnl(value, min, max, protocol):
        '''ensure params are sanitized'''
        if value:
            regex = re.compile(
                r'[a-zA-Z0-9]{' + str(min) + "," + str(max) + "}")
            m = re.match(regex, value)
            if m:
                return m.group().upper()
            if protocol == 'SMS':
                return help_message_sms()
            return help_message_http()

    def sanitize_sec(sec, protocol):
        '''ensure numeric'''
        if sec is not None:
            m = re.match(r'\d{0,3}', str(sec))
            if m:
                return m.group()
            if protocol == 'SMS':
                return help_message_sms()
            return help_message_http()

    def help_message_sms():
        return "Usage: \n Include station and seconds to query\n \
            in the body\n  \
            * sta (required, case insensitive)\n \
            * sec (optional, default 5, max 10)\n \
        example: \n \
            RCM 2 \n \
            RCM"

    def help_message_http():
        return "Usage: \n Include station name in request (case insensitive) \n\
            * sta (required)\n\
            * chan (optional)\n\
            * net (optional)\n\
            * sec (optional, default 5, max 10)\n\
        example: \n\
            /v1.0/sniffwave?sta=RCM&sec=3 \
            /v1.0/sniffwave?sta=RCM"

    def create_sms(msg):
        response = MessagingResponse()
        message = Message()
        message.append(Body("\n" + msg))
        print(msg)
        return str(response.append(message))

    ''' Routes'''
    @app.route('/v1.0/sniffwave', methods=['GET'])
    def get_sniffwave_production():
        return get_sniffwave(EWORM_HOST_PRODUCTION)

    @app.route('/v1.0/staging/sniffwave', methods=['GET'])
    def get_sniffwave_staging():
        return get_sniffwave(EWORM_HOST_STAGING)

    @app.route('/v1.0/sms/sniffwave', methods=['POST'])
    def post_sniffwave_production():
        '''accept sms message only need sta param and seconds'''
        return post_sniffwave(EWORM_HOST_PRODUCTION)

    @app.route('/v1.0/staging/sms/sniffwave', methods=['POST'])
    def post_sniffwave_staging():
        '''accept sms message only need sta param and seconds'''
        return post_sniffwave(EWORM_HOST_STAGING)

    return app
