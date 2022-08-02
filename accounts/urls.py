from django.urls import path
from . import views
urlpatterns = [
    path('register', views.register_view ),
    path('login', views.login_view),
    path('projects/<int:pk>/', views.project_detail_view),
    # path('projects/<int:pk>/users/<int:id>/', views.contributor_detail_view),
    path('projects/<int:pk>/users/', views.contributor_list_create_view),
    path('projects/<int:pk>/users/<int:pk_alt>/', views.contributor_detail_view),

    path('projects', views.project_list_create_view),
    path('delete/user/', views.user_delete_view),
    #  path('user', UserAPIView.as_view()),
    #  path('refresh', RefreshAPIView.as_view()),
    #  path('logout', LogoutAPIView.as_view()),
]


