# bot/views.py
from django.shortcuts import render, redirect
from .forms import BotResponseForm
from .models import BotResponse

def create_bot_response(request):
    if request.method == 'POST':
        form = BotResponseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = BotResponseForm()
    return render(request, 'bot_response_create.html', {'form': form})
