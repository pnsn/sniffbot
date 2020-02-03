
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
DEFAULT_SECONDS = 5


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    EWORM_HOST = app.config['EWORM_HOST']
    EWORM_USER = app.config['EWORM_USER']
    EWORM_RING = app.config['EWORM_RING']

    def help_message(message=None):
        return "Usage: \n Include station and seconds to query \
            in the body\n STA 2"

    def create_sms(msg_short):
        response = MessagingResponse()
        message = Message()
        message.append(Body(msg_short))
        print(msg_short)
        return str(response.append(message))

    @app.route('/v1.0/sniffwave', methods=['GET'])
    def get_sniffwave():
        sta = request.args.get('sta')
        chan = request.args.get('chan')
        net = request.args.get('net')
        loc = request.args.get('loc')
        sec = request.args.get('sec')
        sn = SniffWave(EWORM_HOST, EWORM_USER, EWORM_RING,
                       sta, chan, net, loc, sec)
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
            return help_message()
        try:
            sta, sec = query
        except ValueError:
            sta = query[0].upper()
            sec = DEFAULT_SECONDS
        sn = SniffWave(EWORM_HOST, EWORM_USER, EWORM_RING,
                       sta, None, None, None, sec)
        stdout = sn.call()
        msg_short = sn.format_sms_response(stdout)
        return create_sms(msg_short)

    return app
