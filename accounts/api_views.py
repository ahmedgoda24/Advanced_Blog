# myapp/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login, logout, authenticate
from .serializers import UserSerializer, UserUpdateSerializer,LoginSerializer
from django.contrib.auth.models import User


# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return Response({"message": "Logged in successfully."}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    def post(self, request):
        serialized_request = LoginSerializer(data=request.data)
        if not serialized_request.is_valid():
            return Response(data={'detail': 'البيانات غير صالحة'}, status=status.HTTP_400_BAD_REQUEST)

        username = serialized_request.validated_data.get('username')
        password = serialized_request.validated_data.get('password')
        user = authenticate(request, username=username, password=password)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data={'detail': 'المستخدم غير موجود'}, status=status.HTTP_404_NOT_FOUND)
                
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        login(request, user)

        return Response(
            data={'detail': 'تم  تسجيل الدخول بنجاح',
         'data': { 'token': token.key,}}
         , status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
