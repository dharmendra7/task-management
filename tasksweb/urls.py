from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('', views.project_listing, name='project-listing'),
    path('projects-create', views.create_project, name='project-create'),
    path('projects-details/<int:pk>', views.view_project_details, name='project-details'),
    path('projects-edit/<int:pk>', views.edit_project_details, name='project-edit'),
    path('projects-delete/<int:pk>', views.delete_project, name='project-delete'),
    path('tasks-create/<int:pk>', views.create_task, name='task-create'),
    path('tasks-delete/<int:pk>', views.delete_task, name='task-delete'),
    path('tasks-listing', views.task_listing_for_assignee, name='task-listing'),
    path('tasks-status/<int:pk>', views.change_task_status, name='task-status'),
]