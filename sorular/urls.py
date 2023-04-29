from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('soru_ekle/', views.soru_ekle, name='soru_ekle'),
    path('yorum_ekle/<int:soru_id>/', views.yorum_ekle, name='yorum_ekle'),
    path('arama/', views.arama, name='arama'),
    path('login/', auth_views.LoginView.as_view(template_name='sorular/login.html', success_url=reverse_lazy('anasayfa')), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('baslik_olustur/', views.baslik_olustur, name='baslik_olustur'),
    path('soru_detay/<int:soru_id>/', views.soru_detay, name='soru_detay'),
]
