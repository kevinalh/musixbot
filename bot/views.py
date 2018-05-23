from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def webhook_messenger(request: HttpRequest):
    response = HttpResponse(status = 404)
    if request.method == 'POST':      
        post = request.POST
        response.content = ''
        if 'page' in post.get('object'):
            response.content = 'OK'
            response.status_code = 200
    elif request.method == 'GET':
        verify_token = 'musixbottoken'
        query = request.GET.get('query')
        if 'mode' in query and 'token' in query:
            mode = query['hub.mode'];
            token = query['hub.verify_token'];
            challenge = query['hub.challenge'];
            if mode == 'subscribe' and token == verify_token:
                response.content = challenge
                response.status_code = 200
            else:
                response.status_code = 403
    return response