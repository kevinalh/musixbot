from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests

@csrf_exempt
def webhook_messenger(request: HttpRequest):
    response = HttpResponse(status = 404)
    if request.method == 'POST':
        # Responding to a Messenger request.
        # This is the URL for the Messenger API
        facebook_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='
        facebook_url += settings.PAGE_TOKEN
        post = request.POST
        if 'page' in post.get('object'):
            # Get useful parameters from the sender
            psid = post['sender']['id']
            print(str(psid))
            # Construct the parameters for the API
            param = {}
            message = {}
            recipient = {}
            param['messaging_type'] = 'RESPONSE'
            message['text'] = 'Hello friend!'
            param['message'] = message
            recipient['id'] = psid
            param['recipient'] = recipient
            # Send the JSON response
            requests.post(facebook_url, param)
            # The following response is just to acknowledge the server
            # It's required!
            response.content = 'OK'
            response.status_code = 200
    elif request.method == 'GET':
        # Verification used by Facebook.
        verify_token = 'musixbottoken'
        query = request.GET
        if 'hub.mode' in query and 'hub.verify_token' in query:
            mode = query['hub.mode'];
            token = query['hub.verify_token'];
            challenge = query['hub.challenge'];
            if mode == 'subscribe' and token == verify_token:
                # The token matched! Send the challenge back to verify.
                response.content = challenge
                response.status_code = 200
            else:
                # Forbidden: The token didn't match.
                response.status_code = 403
    return response