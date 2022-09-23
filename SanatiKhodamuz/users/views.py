from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import customUser, work
from django.http import Http404
from django.core.paginator import Paginator

def index(request, page_index = 1):
    latest_work_list = work.objects.order_by('-pub_date')[:5]
    page_lists = Paginator(latest_work_list, 20) 
    if page_index > page_lists.num_pages or page_index < 1:
        raise Http404("page number is out of bounds")
    context = {
        'latest_work_list': page_lists.page(page_index),
        'num_pages': page_lists.num_pages,
        'current_page': page_index,
    }
    page_num_list = [1]
    for i in range(-2, +3):
        p = page_index + i
        if p < page_lists.num_pages and p > 1:
            page_num_list.append(p)
    if page_lists.num_pages > 1:
        page_num_list.append(page_lists.num_pages)
    context['page_num_list'] = page_num_list
    response = render(request, 'users/index.html', context)
    return response
    

def details(request, work_id):
    w = get_object_or_404(work, pk=work_id)
    context = {
        'work': w,
    }
    response = render(request, 'users/details.html', context)
    return response