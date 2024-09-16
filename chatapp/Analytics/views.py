# analytics/views.py
from django.shortcuts import render
from .models import Analytics

def create_analytics(request):
    # Retrieve analytics data from the database
    analytics_data = Analytics.objects.all()
    return render(request, 'analytics_view.html', {'analytics_data': analytics_data})
