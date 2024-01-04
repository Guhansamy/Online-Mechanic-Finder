from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up/',views.signup,name='sign-up'),
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('user_det/',views.user_det,name='user_det'),
    path('profile/<str:user>/',views.profile,name='profile'),
    path('find_mech/',views.find_mech,name='find_mech'),
]
