from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('welcome/', views.welcome_partial, name='load-welcome'),
    path('lists/<int:list_id>/add-task/', views.add_task, name='add-task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete-task'),

]
