from django.urls import path 
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('blog/<int:pk>/', views.post_detail, name='post_detail'),
    path('base', views.render_base),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('login',views.login),
    path('signup',views.signup),
    path('logout', views.logout),
    path('manage/edit/<int:pk>/', views.post_edit),
    path('manage/delete/<int:pk>/', views.post_delete),
]

 
# urlpatterns = [
#     path('', views.post_list),
#     path('blog/<int:pk>/', views.post_detail),
#     path('base', views.render_base),
#     path('manage/post_new', views.post_new),
#     path('login', views.login),
#     path('logout', views.logout),
#     path('manage/edit/<int:pk>/', views.post_edit),
#     path('manage/delete/<int:pk>/', views.post_delete),
#     path('register', views.signup),
# ]
