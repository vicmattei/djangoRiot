"""djangoRiot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static

urlpatterns = [
    re_path(
        '^$', RedirectView.as_view(pattern_name='riot-connector:search'),
        name='redirect'),
    path('admin/', admin.site.urls),
    path(
        'accounts/',
        include(('accounts.urls', 'accounts'), namespace='accounts')),
    path(
        'riot-connecter/',
        include(
            ('riotConnecter.urls', 'riotConnecter'),
            namespace='riot-connector')),
]


if settings.DEBUG:
    urlpatterns.insert(
        0,
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    urlpatterns.insert(
        0,
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))


# reverse('accounts:some_url')
# reverse('namespace:name')
# reverse('some_url')

# camelCase
# snake_case
# cebab-case
# CapitalizedCase
# Titlecase
