from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def webhook_messenger(request: HttpRequest):
    response = HttpResponse(status = 200)
    if request.method == 'POST':
        post = request.POST
    response.content = "This is a default response."
    return response