from django.urls import path
from .views import Create_User_API, User_Login_API, Get_All_Users_API, GetUserById, Referrals_API

urlpatterns = [
    path('createuser', Create_User_API.as_view(), name='create_user'),
    path('login', User_Login_API.as_view(), name='login_user'),
    path('getusers', Get_All_Users_API.as_view(), name='get_users'),
    path('getusersbyid/<str:userid>', GetUserById.as_view(), name='get_user'),
    path('referrals', Referrals_API.as_view(), name='get_user_referrals'),
]