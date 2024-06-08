from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import generics
from .services import *
from .serializers import *


#===================================================================================================================================================================================

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Error logging out.'}, status=status.HTTP_400_BAD_REQUEST)




#отправить код на почту       
class ForgetPasswordSendCodeView(generics.UpdateAPIView):
    serializer_class = SendCodeSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        email_or_phone = request.data.get("email_or_phone")
        if not email_or_phone:
            return Response({"required": "email_or_phone"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email_or_phone=email_or_phone)
            # Если пользователь уже существует, просто обновите его код подтверждения и отправьте его
            send_verification_code(email_or_phone=email_or_phone)
            return Response({"success":"Код был отправлен на почту/телефон"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Если пользователь не существует, создайте нового пользователя и отправьте ему код подтверждения
            user = User.objects.create(email_or_phone=email_or_phone)
            send_verification_code(email_or_phone=email_or_phone)
            return Response({"success":"Код был отправлен на почту/телефон"}, status=status.HTTP_201_CREATED)


# если user забыл пароль при входе
class ForgetPasswordView(generics.UpdateAPIView):
    serializer_class = ForgetPasswordSerializer

    http_method_names = ['patch',]
    def update(self, request, *args, **kwargs):
        
        result = ChangePasswordOnReset.change_password_on_reset(self=self,request=request)

        if result == "success":
            return Response({"success ":"Пароль успешно изменен"}, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)



# ==== User =============================================================================================================================================================

class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserRegisterSerializer


# апи для регистрации
class UserRegisterView(CreateUserApiView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

# апи для логина
class UserLoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')

        if not email_or_phone or not password:
            return Response({'error':'Both email/phone and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email_or_phone=email_or_phone)
        except User.DoesNotExist:
            return Response({'error':'The user does not exist'})
        if not check_password(password, user.password):
            return Response({'error':'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        refresh = RefreshToken.for_user(user=user)
        access_token = refresh.access_token

        user.auth_token_refresh = str(refresh)
        user.auth_token_access = str(access_token)
        user.save()
        
        return Response({
            'detail': 'Successfully confirmed your code',
            'id': user.id,
            'is_seller': user.is_usual,
            'email': user.email_or_phone,
            'refresh': str(refresh),
            'access': str(access_token),
            'refresh_lifetime_days': refresh.lifetime.days,
            'access_lifetime_seconds': access_token.lifetime.total_seconds()
        })




# апи который проверяет код который был отправлен на указанный email и в ответ передает токен
class UserVerifyRegisterCode(generics.UpdateAPIView):
    serializer_class = VerifyCodeSerializer

    http_method_names = ['patch',]
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        

        return CheckCode.check_code(code=code,)
    


class UserInfoApiView(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = User.objects.filter(id=user.id).first()
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)
    


class UserUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all() 
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]





from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from django.contrib.auth.hashers import make_password
from django.utils.crypto import constant_time_compare


class ChangePasswordUserAPIVIew(UpdateModelMixin, GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = User.objects.get(id=self.request.user.id)
        return user

    def patch(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            new_password = self.request.data.get('new_password')
            confirming_new_password = self.request.data.get('confirming_new_password')
            if constant_time_compare(new_password, confirming_new_password):
                user = self.get_object()
                user.password = make_password(confirming_new_password)
                user.save()
                return Response({'Вы ушпешно поменяли свой пароль'}, status=status.HTTP_200_OK)
            else:
                return Response({'Пароли не совподают'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)

