from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import customUser, work
from django.http import Http404
from django.core.paginator import Paginator

def index(request, page_index = 1):
    latest_work_list = work.objects.order_by('-pub_date')[:5]
    page_lists = Paginator(latest_work_list, 1) 
    if page_index > page_lists.num_pages or page_index < 1:
        raise Http404("page number is out of bounds")
    context = {
        'latest_work_list': page_lists.page(page_index),
        'num_pages': page_lists.num_pages,
        'current_page': page_index,
    }
    if (page_index < page_lists.num_pages):
        context['next_page'] = page_index + 1 
    if (page_index > 1):
        context['previous_page'] = page_index - 1
    return render(request, 'users/index.html', context)

def detail(request, work_id):
    w = get_object_or_404(work, pk=work_id)
    context = {
        'work': w,
    }
    return render(request, 'users/detail.html', context)
