from django.shortcuts import render
from django.http import HttpResponse

def auth(request):
    return render(request, 'reviews/auth.html')
