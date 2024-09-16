# conversation/views.py
from django.shortcuts import render, redirect
from .forms import UserPreferenceForm
from .models import UserPreference

def create_user_preference(request):
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = UserPreferenceForm()
    return render(request, 'user_preference_create.html', {'form': form})
