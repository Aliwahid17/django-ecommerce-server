from django.shortcuts import render , HttpResponse
from .tasks import test_task

# Create your views here.

def run_task(request):
    test_task.delay()
    return HttpResponse("Done")