# conversation/views.py
from django.shortcuts import render, redirect
from .forms import MessageForm
from .models import Message

def create_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = MessageForm()
    return render(request, 'message_create.html', {'form': form})
