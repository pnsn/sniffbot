
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


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])

    def help_message(message=None):
        return "Usage: \n Include station and seconds to query \
            in the body\n STA 2"

    def create_sms(msg):
        response = MessagingResponse()
        message = Message()
        message.append(Body(msg))
        print(msg)
        return str(response.append(message))

    @app.route('/v1.0/sniffwave', methods=['GET'])
    def get_sniffwave():
        sta = request.args.get('sta').uppper()
        sn = SniffWave(sta)
        response = sn.parse_log()
        return response

    @app.route('/v1.0/sms/sniffwave', methods=['POST'])
    def post_sniffwave():
        '''accept sms message

            only need sta param and seconds
        '''
        body = request.form['Body']
        query = body.split()
        if not query:
            return help_message()
        sta = query[0].upper()
        sn = SniffWave(sta)
        msg = sn.parse_log()
        response = create_sms(msg)

        return response

    return app
