import random
import string
from django.contrib.auth.hashers import make_password
from django.db import models, transaction
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User, Referral
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


def generate_referral_code(username):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f"{username}_{random_string}_magicpitch"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'referral_code']

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        referral_code = data.get('referral_code')

        if not username:
            raise serializers.ValidationError('Please provide a username')

        if not email:
            raise serializers.ValidationError('Please provide an email address')

        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            raise serializers.ValidationError('User with this email address already exists')

        password = data.get('password')
        data['password'] = make_password(password)

        if not referral_code:
            data['referral_code'] = generate_referral_code(username)

        return data



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError('Please enter "email" and "password".')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if user:
                    refresh = RefreshToken.for_user(user)

                    return {
                            'message': 'Login successful.',
                            'username': user.username,
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                            }
            else:
                raise serializers.ValidationError('Incorrect email or password.')
        else:
            raise serializers.ValidationError(' Please enter "email" and "password".')


class GetUserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User
        fields = ['id', 'username', 'email', 'referral_code', 'points', 'created_at', 'updated_at']



class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'


class GetUserbyidSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    referrals_made = ReferralSerializer(many=True, source='referrals_made.all')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'referral_code', 'points', 'created_at', 'updated_at', 'referrals_made']



class Referral_Serializer(serializers.ModelSerializer):
    referrer_username = serializers.SerializerMethodField()
    referred_username = serializers.SerializerMethodField()

    class Meta:
        model = Referral
        fields = ['referral_code_used', 'created_at', 'referrer_username', 'referred_username']

    def get_referrer_username(self, obj):
        return obj.referrer.username

    def get_referred_username(self, obj):
        return obj.referred_user.username