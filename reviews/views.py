from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Ticket
from .forms import CreateTicketForm


@login_required
def create_ticket(request):
    form = CreateTicketForm()

    if request.method == "POST":
        form = CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = request.FILES['image']
            user = request.user
            
            ticket = Ticket(title=title, description=description, image=image, user=user)
            ticket.save()
            return redirect('reviews:feeds')

    context = {
        'form': form,
    }
    return render(request, 'reviews/create_ticket.html', context)


@login_required
def feeds(request):
    context = {
        'media_url': settings.MEDIA_URL,
    }
    return render(request, 'reviews/feeds.html', context)
