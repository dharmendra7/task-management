from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib import auth

from .common import *
from .serializers import *
from .models import *

def get_user(request):
    token = request.headers['Authorization']
    print(token)
    access_token_obj = AccessToken(token)
    user_id = access_token_obj['user_id']
    user = User.objects.get(id=user_id)

    return user

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            password = request.data['password']
            email = request.data['email'].lower()
            user_info = User.objects.filter(email=email)
            
            if user_info.exists():
                user = auth.authenticate(email=email, password=password)
                user_obj = User.objects.get(email=email)
                
                if user_obj.is_active == False:
                    return error_401(request, message='Account disabled, please contact an administrator.', code=401)

            else:
                return error_401(request, message='Incorrect email address or password.', code=401)
            
            if user == None:
                return error_401(request, message='Incorrect email address or password.', code=401)

            token = {'refresh': user.tokens()['refresh'],
                     'access': user.tokens()['access']}

            return send_response(request, message=("You are logged in successfully"), data=token)
        
        except Exception as e:
            return error_400(request, message=str(e))


class ListProject(generics.GenericAPIView):

    def get(self, request):
        try:
            print('working')
            projects = Project.objects.all()
            respone = [{
                "id" : value.id,
                "name": value.name,
                "descr" : value.description,
                "created_at" : value.created_at 
                }for value in projects]
            return JsonResponse(respone, safe=False)
        except Exception as e:
            return error_400(request, message=str(e))


class CreateProject(generics.GenericAPIView):
    serializer_class = ProjectCreateSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'user': get_user(request)}) # need to add context to get user id in serializer class
            if serializer.is_valid():
                serializer.save()
                return send_response_validation(request, code=200, message=("Project added successfully"))
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return send_response_validation(request, code=2001, message=(error_msg_value[0]))
            
        except Exception as e:
            return error_400(request, message=str(e))


class DeleteProject(generics.GenericAPIView):
    def delete(self, request):
        try:
            project_id = request.GET.get('project_id', None)
            
            if project_id:
                if Project.objects.filter(id = project_id).exists():
                    project_obj = Project.objects.get(id = project_id)
                    project_obj.delete()
                    return JsonResponse({
                        'message' : 'Project is deleted successfully.'
                    })
                else:
                    return error_400(request, message="project_id does not exist")
            else:
                return error_400(request, message="Please add a valid project_id")

        except Exception as e:
            return error_400(request, message=str(e))


class EditProject(generics.GenericAPIView):
    serializer_class = ProjectEditSerializer

    def put(self, request):
        try:
            serializer = self.serializer_class(data=request.data,context={'user': get_user(request)})
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return JsonResponse({
                        "message" : "Project is edited succesfully"
                })
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))
        
        except Exception as e:
            return error_400(request, message=str(e))

from rest_framework.response import Response

class ListTask(generics.GenericAPIView):
    def get(self, request):
        # try:
            project_id = request.GET.get('project_id', None)
            
            if project_id:
                if Project.objects.filter(id = project_id).exists():
                    task_obj = Task.objects.filter(project = project_id)
                    respone = [{
                        "id" : value.id,
                        "name": value.name,
                        "descr" : value.description,
                        "assign_to" : value.assign_to,
                        "status" : value.completed,
                        "created_at" : value.created_at 
                        }for value in task_obj]
                    print(respone)
                    return JsonResponse({'data' : respone})
                else:
                    return error_400(request, message="project_id does not exist")
            else:
                return error_400(request, message="Please add a valid project_id")

        # except Exception as e:
        #     return error_400(request, message=str(e))


class CreateTask(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'user': get_user(request)})
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return JsonResponse({
                            "message" : "Task is created succesfully"
                    })
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))
        except Exception as e:
            return error_400(request, message=str(e))


class EditTask(generics.CreateAPIView):
    serializer_class = TaskEditSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'user': get_user(request)})
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return JsonResponse({
                            "message" : "Task is edited succesfully"
                    })
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))
        except Exception as e:
            return error_400(request, message=str(e))

class DeleteTask(generics.GenericAPIView):
    def delete(self, request):
        try:
            task_id = request.GET.get('task_id', None)
            
            if task_id:
                if Task.objects.filter(id = task_id).exists():
                    task_obj = Task.objects.get(id = task_id)
                    task_obj.delete()
                    return JsonResponse({
                        'message' : 'Task is deleted successfully.'
                    })
                else:
                    return error_400(request, message="Task does not exist")
            else:
                return error_400(request, message="Please add a valid task_id")

        except Exception as e:
            return error_400(request, message=str(e))


