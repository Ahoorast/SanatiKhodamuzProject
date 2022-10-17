from ast import AsyncFunctionDef
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import customUser, work, jobAssignments
from django.contrib.auth.models import User
from django.http import Http404
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test

from .tokens import account_activation_token
from django.views.decorators.cache import cache_page
from django.http import JsonResponse


user_login_required = user_passes_test(lambda user: user.is_active, login_url='/users')
user_must_be_employer = user_passes_test(lambda user: user.is_active and customUser.objects.get(user=user).isEmployer, login_url='/users')
user_must_be_employee = user_passes_test(lambda user: user.is_active and not customUser.objects.get(user=user).isEmployer, login_url='/users')

def active_user_required(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func

def employer_user_required(view_func):
    decorated_view_func = login_required(user_must_be_employer(view_func))
    return decorated_view_func

def not_employer_user_required(view_func):
    decorated_view_func = login_required(user_must_be_employee(view_func))
    return decorated_view_func

def addUserDataToContext(request, context):
    if request.user.is_authenticated:
        context['logged_in'] = True
        context['user'] = request.user
        context['cuser'] = customUser.objects.get(user=request.user)
    else:
        context['logged_in'] = False
    return context

def index(request):
    latest_work_list = work.objects.all()[0:5]
    context = {
        'latest_work_list': latest_work_list,
    }
    context = addUserDataToContext(request, context)
    response = render(request, 'users/index.html', context)
    return response

def loadMore(request):
    last_work_index = request.GET.get('last_work_index')
    last_work_index = int(last_work_index)
    tmp_latest_work_list = work.objects.all()[last_work_index:last_work_index+5]
    latest_work_list = []
    for w in tmp_latest_work_list: 
        wDic = {}
        wDic['id'] = w.id
        wDic['title'] = w.title
        wDic['price'] = w.price
        wDic['show_estimate'] = w.show_estimate()
        print(w.show_estimate())
        wDic['employer'] = w.employer.user.username
        latest_work_list.append(wDic)
    data = {
        'latest_work_list': latest_work_list,
    }
    response = JsonResponse(data=data)
    return response

def details(request, work_id):
    w = get_object_or_404(work, pk=work_id)
    context = {
        'work': w,
    }
    context = addUserDataToContext(request, context)
    response = render(request, 'users/details.html', context)
    return response

def activateEmail(request, user, to_email): 
    mail_subject = 'Activate your user account.'
    message = render_to_string('../templates/activate_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    if send_mail(
        mail_subject,
        message, 
        'SamaneAnjameKar@gmail.com',
        [to_email],
        fail_silently=False,
    ):
        messages.success(request, f'Dear {user},     please go to you email {to_email} inbox and click on \
       received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def usernameAlreadyExistsMessage(request, username):
    messages.error(request, f'the username {username} already exists')

def signupView(request):
    try:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_rpt = request.POST['password_rpt']
        employer = False
        if request.POST.get('master'):
            employer = True
    except (KeyError or username.DoesNotExist or email.DoesNotExist or password.DoesNotExist or password_rpt.DoesNotExist):
        return HttpResponse("error")
    else:
        if password != password_rpt:
            messages.error(request, f'password should match its repitition')
            return HttpResponseRedirect(reverse('users:index'))
        if User.objects.filter(username=username):
            messages.error(request, f'username is not available')
            return HttpResponseRedirect(reverse('users:index'))
        user = User.objects.create_user(username, email, password)
        user.is_active = False
        user.save()
        cu = customUser(user=user, isEmployer=employer)
        cu.save()
        activateEmail(request, user, email)
        return index(request)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return index(request)
    else:
        messages.error(request, 'Activation link is invalid!')
        return index(request)

def loginView(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except (KeyError, username.DoesNotExist or password.DoesNotExist):
        messages.error(request, "error: incorrect password")
        return HttpResponseRedirect(reverse('users:index'))
    else:  
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'error: incorrect password')
            return HttpResponseRedirect(reverse('users:index'))
        if user.is_active == False:
            messages.error(request, 'you must first activate your account')
            return HttpResponseRedirect(reverse('users:index'))
        login(request, user)
        messages.success(request, 'you\'ve logged in succsessfuly')
        return index(request)

@login_required(login_url='/users')
def logoutView(request):
    logout(request)
    return index(request)

@user_must_be_employer
def addWork(request):
    context = {}
    context['user'] = request.user
    try:
        title = request.POST['title']
        price = request.POST['price']
        description = request.POST['description']
        estimate = request.POST['estimate']
    except (KeyError):
        response = render(request, 'users/new_task.html', context)
        return response
    else:
        employer = customUser.objects.get(user=request.user)
        w = work(employer=employer, title=title, price=price, description=description, estimate=estimate)
        w.save()
        print(w)
        return index(request)

@user_must_be_employee
def assignJobToUser(request, work_id):
    user = request.user
    w = work.objects.get(pk=work_id)
    if work:
        if jobAssignments.objects.filter(employee=user):
            messages.error(request, 'you have already applied for a job')
        elif jobAssignments.objects.filter(job=w):
            messages.error(request, 'the job has already been applied for by another user')
        else:
            jobAssignment = jobAssignments(job=w, employee=user)
            jobAssignment.save()
            messages.success(request, 'you have succsessfully assigned this job to you')
    else:
        messages.error(request, 'given work_id does not exist')
    return index(request)
