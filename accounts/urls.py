from django.urls import path
from . import views
urlpatterns = [
    path('register', views.register_view ),
    path('login', views.login_view),
    path('projects/<int:pk>/', views.project_detail_view),
    # path('projects/<int:pk>/users/<int:id>/', views.contributor_detail_view),
    path('projects/<int:pk>/users/', views.contributor_list_create_view),
    path('projects/<int:pk>/users/<int:pk_alt>/', views.contributor_detail_view),
    path('projects/<int:pk>/issues/<int:pk_alt>/', views.issue_detail_view),
    path('projects/<int:pk>/issues/', views.issue_list_create_view),
    path('projects/<int:pk>/issues/<int:pk_alt>/comments/', views.comment_list_create_view),
    path('projects/<int:pk_project>/issues/<int:pk_issue>/comments/<int:pk_comment>/', views.comment_detail_view),
    path('projects', views.project_list_create_view),
    path('delete/user/', views.user_delete_view),
]


