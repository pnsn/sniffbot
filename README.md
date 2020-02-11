# sniffbot
An SMS and HTTP wrapper for Earthworm utilities

## HTTP
`/v1.0/sniffwave GET`

Query Params, all optional
* sta: default = 'wild'
* chan: default = 'wild'
* net: default = 'wild'
* sec: defualt = 3, max 5  (number of seconds for sniffwave request)

Example query:
`/v1.0/sniffwave?sta=RCM&sec=2
## SMS 
Uses the [Twilio API](https://www.twilio.com). 
### Twilio configuration
First purchase a twilio phone number, ~$1/month. Next go to Phone numbers, select phone number and in the Messaging form, add your api url to "A message comes in". Select "Webhook" and "HTTP POST" in the select list for this field. Note, Twilio will only forward to HTTPS. 
### USAGE
Text STA and sec(optional) to sniffbot #

### Local development
To test using the [Twilio API](https://www.twilio.com) you need to create a tunnel to your dev box localhost

[ngrok](https://ngrok.com) will allow you to do this. You need to create an account and recieve an endpoint url. 
[Configuration details here](https://www.twilio.com/blog/2013/10/test-your-webhooks-locally-with-ngrok.html)
`./ngrok http 5000`

