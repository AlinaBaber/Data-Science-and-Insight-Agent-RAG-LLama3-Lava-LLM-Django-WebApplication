# conversation/views.py
from django.shortcuts import render, redirect
from .forms import ConversationForm

def create_conversation(request):
    if request.method == 'POST':
        form = ConversationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = ConversationForm()
    return render(request, 'conversation_create.html', {'form': form})





