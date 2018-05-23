from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def webhook_messenger(request: HttpRequest):
    response = HttpResponse(status = 200)
    post = request.POST
    response.content = ''
    if 'page' in post.get('object'):
        response.content = 'OK'
    return response