from django.urls import path
from .views import * 

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('edit-project', EditProject.as_view(), name='edit-project'),
    path('get-project', ListProject.as_view(), name='get-project'),
    path('create-project', CreateProject.as_view(), name='create-project'),
    path('delete-project', DeleteProject.as_view(), name='delete-project'),
    path('get-task', ListTask.as_view(), name='get-tasks'),
    path('edit-task', EditTask.as_view(), name='edit-task'),
    path('create-task', CreateTask.as_view(), name='create-task'),
    path('delete-task', DeleteTask.as_view(), name='delete-task'),
]