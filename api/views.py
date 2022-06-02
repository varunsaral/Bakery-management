from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserCreateSerializer, UserLoginSerializer
from .renderer import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegister(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'msg':'Registion success','token':token},status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class UserLogin(APIView):
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            print(user)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg':'Login Success','token':token},status=status.HTTP_200_OK)
            else :
                return Response({'errors':{'non_fields_error':['Email or password is not valid']}})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    