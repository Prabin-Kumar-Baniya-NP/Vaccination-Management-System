"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from .views import index


urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path("accounts/", include("user.urls", namespace="accounts")),
    path("center/", include("center.urls", namespace="center")),
    path("vaccine/", include("vaccine.urls", namespace="vaccine")),
    path("campaign/", include("campaign.urls", namespace="campaign")),
    path("vaccination/", include("vaccination.urls", namespace="vaccination")),
]

# Static and Media File URL
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

# Django - Rosetta URL
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path("rosetta/", include('rosetta.urls'))
    ]

# Password Reset Url Paths
urlpatterns += [
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

# Django Admin Panel Customization
admin.site.site_header = "Book My Vaccine"
admin.site.site_title = "Book My Vaccine | Admin"
admin.site.index_title = "Admin Panel"
