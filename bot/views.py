from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def webhook_messenger(request: HttpRequest):
    response = HttpResponse(status = 404)
    if request.method == 'POST':
        # Responding to a Messenger request.
        post = request.POST
        response.content = ''
        if 'page' in post.get('object'):
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