from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('profile/<int:pk>', views.Profile.as_view(), name='profile'),
    path('create/', views.CreateUser.as_view(), name='create'),
    path('thanks/', views.Thanks.as_view(), name='thanks'),
    path('complete/<str:token>', views.CompleteCreationUser.as_view(), name='complete_creation'),
    path('account-settings/<int:pk>', views.AccountSettings.as_view(), name='account_settings'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('mypage/<int:pk>', views.MyPage.as_view(), name='mypage'),
    path('change-password/<int:pk>', views.ChangePassword.as_view(), name='change_password')
]
