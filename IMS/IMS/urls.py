"""
URL configuration for IMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# IMS/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth
from django.urls import include, path
from inventory.views import CustomPasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),  # Assuming this is the app's URL configuration   
    path('', auth.LoginView.as_view(template_name="inventory/login.html"), name='login'),
    path("logout/",auth.LogoutView.as_view(template_name="inventory/logout.html"),name="logout"),
    path('reset_password/', CustomPasswordResetView.as_view(template_name="inventory/forget.html"), name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="inventory/reset.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="inventory/set_password.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="inventory/set_password_confirm.html"),name="password_reset_complete")







] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
