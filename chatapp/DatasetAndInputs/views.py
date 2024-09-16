# conversation/views.py
from django.shortcuts import render, redirect
from .forms import DatasetAndInputsForm
from .models import DatasetandInput

def create_dataset_and_inputs(request):
    if request.method == 'POST':
        form = DatasetAndInputsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = DatasetAndInputsForm()
    return render(request, 'dataset_and_inputs_create.html', {'form': form})
