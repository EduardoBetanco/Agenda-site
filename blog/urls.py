from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
]