from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.upload_image, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('ocr/', views.upload_image, name='upload_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


