"""maxapi URL Configuration

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
from maxapi import views

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('accounts.urls')),
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # Project Views
#     path('projects/', views.project_list),
#     path('projects/<int:id>', views.project_detail),
#     # Contributor Views
#     path('contributors/', views.contributor_list),
#     path('contributors/<int:id>', views.contributor_detail),
#     # Comment Views
#     path('comments/', views.comment_list),
#     path('comments/<int:id>', views.comment_detail),
#     # Issue Views
#     path('issues/', views.issue_list),
#     path('issues/<int:id>', views.issue_detail),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)

