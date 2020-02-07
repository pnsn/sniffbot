'''
Where all the magic happens again, and again and again
'''
from flask import request, Flask, abort
from .config import app_config
from .models import SniffWave
from twilio.twiml.messaging_response import (
    MessagingResponse,
    Message,
    Body
)
import re

DEFAULT_SECONDS = 5


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    EWORM_HOST = app.config['EWORM_HOST']
    EWORM_USER = app.config['EWORM_USER']
    EWORM_RING = app.config['EWORM_RING']
    SSH_I_FILE = app.config['SSH_I_FILE']

    def sanitize_scnl(value, min, max):
        '''ensure params are sanitized'''
        if value:
            regex = re.compile(
                r'[a-zA-Z0-9]{' + str(min) + "," + str(max) + "}")
            m = re.match(regex, value)
            if m:
                return m.group().upper()
            abort(400, value)

    def sanitize_sec(sec):
        '''ensure numeric'''
        if sec is not None:
            m = re.match(r'\d', str(sec))
            if m:
                return m.group()
            abort(400, sec)

    def help_message_sms():
        return "Usage: \n Include station and seconds to query \
            in the body\n STA 2"

    def help_message_http():
        return "Usage: \n Include at least one query param needed\n\
            * sta (required)\n\
            * chan (optional)\n\
            * net (optional)\n\
            * sec (optional, default 5, max 10)\n\
        example: \n\
            /v1.0/sniffwave?sta=RCM&sec=3"

    def create_sms(msg):
        response = MessagingResponse()
        message = Message()
        message.append(Body("\n" + msg))
        print(msg)
        return str(response.append(message))

    @app.route('/v1.0/sniffwave', methods=['GET'])
    def get_sniffwave():
        sta = sanitize_scnl(request.args.get('sta'), 3, 5)
        if len(request.args) < 1 or sta is None:
            return help_message_http()
        chan = sanitize_scnl(request.args.get('chan'), 3, 3)
        net = sanitize_scnl(request.args.get('net'), 2, 2)
        sec = request.args.get('sec')
        if sec is not None:
            sec = min(sec, 10)
            sec = sanitize_sec(sec)
        sn = SniffWave(EWORM_HOST, EWORM_USER, EWORM_RING,
                       SSH_I_FILE, sta, chan, net, sec)
        stdout = sn.call()
        print(stdout.split('\n'))
        return stdout

    @app.route('/v1.0/sms/sniffwave', methods=['POST'])
    def post_sniffwave():
        '''accept sms message

            only need sta param and seconds
        '''
        body = request.form['Body']
        query = body.split()
        if not query:
            return help_message_sms()
        try:
            sta, sec = query
        except ValueError:
            sec = str(DEFAULT_SECONDS)
        sta = sanitize_scnl(query[0].upper(), 3, 5)
        if sec is not None:
            sec = min(int(sec), 10)
            sec = sanitize_sec(sec)
        sn = SniffWave(EWORM_HOST, EWORM_USER, EWORM_RING,
                       SSH_I_FILE, sta, None, None, sec)
        stdout = sn.call()
        msg = sn.format_sms_response(stdout)
        return create_sms(msg)

    return app
