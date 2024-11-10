from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
def homepage(request):
    return render(request,'home.html')

@never_cache
@login_required
def aboutpage(request):
    return render(request,'about.html')