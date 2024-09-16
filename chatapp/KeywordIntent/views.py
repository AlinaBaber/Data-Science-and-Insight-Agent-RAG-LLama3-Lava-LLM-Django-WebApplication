# bot/views.py
from django.shortcuts import render, redirect
from .forms import KeywordIntentForm
from .models import KeywordIntent

def create_keyword_intent(request):
    if request.method == 'POST':
        form = KeywordIntentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = KeywordIntentForm()
    return render(request, 'keyword_intent_create.html', {'form': form})
