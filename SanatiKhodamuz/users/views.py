from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import customUser, work
from django.http import Http404

def index(request):
    latest_work_list = work.objects.order_by('-pub_date')[:5]
    context = {
        'latest_work_list': latest_work_list,
    }
    return render(request, 'users/index.html', context)

def detail(request, work_id):
    w = get_object_or_404(work, pk=work_id)
    return render(request, 'users/detail.html', {'work': w})
