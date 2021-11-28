from django.urls import path
from django.urls.conf import include
from videocallingapplocation import views

urlpatterns = [
    path('', views.index,name='index'),
    path('login/',views.loginuser,name='login'),
    path('logout/',views.logoutuser,name='logout'),
    path('register/',views.register,name='register'),
    path('room/<str:room_name>/',views.room,name='room')
]
