from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def list_reports(request):
    return render(request, 'reports.html', {'active_page': 'reports'})