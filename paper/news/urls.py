
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('post/<int:post_pk>/', article, name='post'),
    path('create/', create_post, name='create'),
    path('delete/<int:post_pk>/', delete_post, name='delete'), 
    path('update/<int:post_pk>/', update_post, name='update'),
    path('category/<slug:cat_slug>/', categories, name='category'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('self_user_profile/', self_user_profile, name='self_user_profile'),
    path('edit_profile', UserEditView.as_view(), name='edit_profile'),
    path('user_profile/<int:user_pk>/', user_profile, name='user_profile'),
    path('delete_comment/<int:comment_pk>', delete_comment, name='delete_comment'),
]
