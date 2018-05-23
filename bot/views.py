from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import json

@csrf_exempt
def webhook_messenger(request: HttpRequest):
    response = HttpResponse(status = 404)
    if request.method == 'POST':
        # Responding to a Messenger request.
        # This is the URL for the Messenger API
        facebook_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='
        facebook_url += settings.PAGE_TOKEN
        query = request.body
        query = json.loads(query)
        if 'object' in query:
            response.status_code = 200
            if query['object'] == 'page':
                [post] = query['entry'][-1]['messaging']
                # Get useful parameters from the sender
                psid = post['sender']['id']
                # Construct the parameters for the API
                param = {}
                message = {}
                recipient = {}
                param['messaging_type'] = 'RESPONSE'
                message['text'] = 'Hello friend!'
                param['message'] = message
                recipient['id'] = psid
                param['recipient'] = recipient
                # Use the API and save the response in a variable
                facebook_response = requests.post(facebook_url, json = param)
                response.status_code = facebook_response.status_code
        # The following response is just to acknowledge the server
        # It's required!
        else:
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