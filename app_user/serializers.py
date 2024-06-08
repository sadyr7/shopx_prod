from rest_framework import serializers
from .models import User
from product.serializers import Product
from Category.serializers import CategorySerializer, PodCategorySerializer
from django.core.exceptions import ValidationError
import re



class UserRegisterSerializer(serializers.ModelSerializer):
    email_or_phone = serializers.EmailField(required=True)
    password_confirm = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)
    username = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['email_or_phone','username','password','password_confirm']

    # def validate_email_or_phone(self, value):
    #     # Проверяем, является ли значение адресом электронной почты
    #     if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
    #         return value
    #     # Проверяем, является ли значение номером телефона
    #     elif re.match(r'^\+996\d{9}$', value):   # Примерный шаблон номера телефона, подставьте свой
    #         return value
    #     # Если значение не соответствует ни адресу электронной почты, ни номеру телефона, вызываем ошибку
    #     else:
    #         raise serializers.ValidationError("Invalid email address or phone number.")

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")

        email_or_phone = attrs.get('email_or_phone')
        if email_or_phone:
            if '@' in email_or_phone:
                attrs['email'] = email_or_phone
            else:
                raise serializers.ValidationError("only email")
                # try:
                #     phone_number = email_or_phone  # Замените на вашу собственную логику проверки номера телефона
                #     attrs['phone_number'] = phone_number
                # except ValidationError:
                #     raise serializers.ValidationError("Неверный формат номера телефона")
        return attrs
    

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except:
            raise serializers.ValidationError({"dublicate":"user exists!"})
        
    

class BecomeUserSerializer(serializers.Serializer):


    def create(self, validated_data):
        # Проверяем, если флажок is_usual установлен в True, создаем объект класса User
        if validated_data.get('is_usual', False):
            return User.objects.create(**validated_data)
        # Если флажок is_usual установлен в False или не передан, создаем объект SellerProfile
        return User.objects.create(**validated_data)

class VerifyCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        ref_name = "UserVerify" 
        model = User
        fields = ['code']


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    email_or_phone = serializers.CharField(required=True)
    
    class Meta:
        ref_name = "UserLogin" 
        model = User
        fields = ['email_or_phone','password']
    
    def validate(self, attrs):
        email_or_phone = attrs.get('email_or_phone')
        password = attrs.get('password')

        if not email_or_phone or not password:
            raise serializers.ValidationError("Both email/phone and password are required")

        return attrs


class ChangePasswordSerializer(serializers.Serializer): 
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ['new_password',
                  'confirm_new_password',]

class SendCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        ref_name = "UserCode" 
        model = User
        fields = ['email_or_phone']


class ForgetPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6,write_only=True)
    password = serializers.CharField(max_length=20,write_only=True)
    confirm_password = serializers.CharField(max_length=20,write_only=True)

    class Meta:
        ref_name = "UserForget" 
        fields = ['password','confirm_password','code']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["__all__"]


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
                'id',
                'username',
                'surname',
                'email_or_phone',
                'image'
                  ]

class UserRecallSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
                'id',
                'username',
                'image'
                  ]
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    class Meta:
        ref_name = "UserLogout" 
        fields = ['refresh_token',]