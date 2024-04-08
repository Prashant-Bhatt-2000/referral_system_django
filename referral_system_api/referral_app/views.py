from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializer import UserSerializer, UserLoginSerializer, GetUserSerializer, ReferralSerializer, Referral_Serializer
from .models import User, Referral
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator


class Create_User_API(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data
        serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()
            points_earned = 0
            if user_data.get('referral_code'):
                referred_user = User.objects.filter(referral_code=user_data['referral_code']).first()
                if referred_user:
                    referred_user.points += 1
                    referred_user.referred_to = user.id
                    referred_user.save()
                    points_earned = 1

                    referral_data = Referral.objects.create(
                        referrer=referred_user,
                        referred_user=user,
                        referral_code_used=user_data['referral_code'] 
                    )


            return Response({'message': 'User created', 'user': serializer.data, 'points_earned': points_earned}, status=status.HTTP_201_CREATED)

        return Response({'message': 'Validation errors', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class User_Login_API(APIView):
    def post(self, request):
            data = request.data
            serializer = UserLoginSerializer(data=data)
            if serializer.is_valid():
                response_data = serializer.validated_data
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class Get_All_Users_API(APIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = User.objects.all()

        if users: 
            serializer = GetUserSerializer(users, many=True)
            return Response(serializer.data)
    
        return Response({ 'message': 'No users Found'}, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import get_object_or_404


class GetUserById(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, userid):
        user = get_object_or_404(User, id=userid)
        serializer = GetUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Referrals_API(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user 
        referrals = Referral.objects.filter(referral_code_used=user.referral_code).order_by('-created_at')
        
        paginator = Paginator(referrals, 20) 
        page_number = request.query_params.get('page')
        page_referrals = paginator.get_page(page_number)
        
        serializer = Referral_Serializer(page_referrals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

