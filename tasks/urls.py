from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),  # Homepage for tasks
    path('create/', views.create_task, name='create_task'),  # Page to add a task
]