from django.shortcuts import render
from django.http import HttpResponse

def auth(request):
    return render(request, 'reviews/auth.html')

def register(request):
    return render(request, 'reviews/register.html')

def create_ticket(request):
    return render(request, 'reviews/create_ticket.html')