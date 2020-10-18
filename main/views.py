from django.shortcuts import render, redirect, get_list_or_404
from .models import Blurb, BlurbForm

# Create your views here.

def index(request):
    if request.method == 'POST':
        new_blurb = BlurbForm(request.POST)
        new_blurb.save()
        return redirect('main:index')
    blurbs = get_list_or_404(Blurb)
    return render(request, 'main/index.html', {'blurbs': blurbs})