from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # ex: /users/
    path('', views.index, name='index'),
    path('page/<int:page_index>/', views.index, name='index_by_page'),
    path('job/<int:work_id>/', views.details, name='details'),
]