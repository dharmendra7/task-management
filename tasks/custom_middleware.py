from rest_framework_simplejwt.tokens import AccessToken
from .common import *
from .models import *


url=['/api/create-project', '/api/get-project', '/api/delete-project', '/api/edit-project', '/api/get-task', '/api/create-task', '/api/edit-task', '/api/delete-task']
def authentication_middleware(get_response):
    def middleware(request):
        if request.path in url:
            if "Authorization" in request.headers.keys():
                data=(request.headers)
                try:
                    tokens = data['Authorization']
                    access_token_obj = AccessToken(tokens)
                except:
                    return error_401(request,message="Invalid Token. You are not authenticated to access this endpoint")
            else:
                return error_401(request,message="Please provide authentication token")
        response = get_response(request)
        return response  

    return middleware