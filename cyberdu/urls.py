from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from main.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),

    # Кастомная страница входа
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=LoginForm
        ),
        name='login'
    ),

    # Стандартные маршруты авторизации Django
    path('accounts/', include('django.contrib.auth.urls')),

    # Маршруты приложения main
    path('', include('main.urls')),
]

# Подключение static и media файлов в режиме разработки
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)