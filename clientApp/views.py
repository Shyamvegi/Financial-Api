from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.models import AuthToken
from knox.views import LoginView,LogoutView

from .serializers import UserSerializer, RegisterSerializer ,LoginUserSerializer
from django.contrib.auth import login

# View For New User Registration

class Signup(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data={
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        }
        
        return Response(data)

#API for login

class Login(LoginView):
    permission_classes=(permissions.AllowAny,)
    serializer_class = LoginUserSerializer
    def post(self, request, format=None):
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            return super(Login, self).post(request, format=None)
            '''
            except Exception as e:
            errdata = {"message": str(e)}
            return Response(errdata, status=400)
            '''

class Logout(LogoutView):

    def post(self, request, format=None):
        try:
            request._auth.delete()
            user_logged_out.send(sender=request.user.__class__,
                                 request=request, user=request.user)
            return Response({"message":"logged out successfully"}, status=200)
        except Exception as e:
            errdata={"message":str(e)}
            return Response(errdata,status=400)


class Userdetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
