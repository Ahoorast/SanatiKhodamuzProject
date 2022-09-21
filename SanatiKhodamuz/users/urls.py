from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # ex: /users/
    path('', views.index, name='index'),
    # ex: /users/5/
    path('<int:work_id>/', views.detail, name='detail'),
]