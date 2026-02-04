from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/new/', views.task_new, name='task_new'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:pk>/toggle_done/', views.task_toggle_done, name='task_toggle_done'),
    path('task/<int:pk>/toggle-ajax/', views.task_toggle_done_ajax, name='task_toggle_done_ajax'),

]