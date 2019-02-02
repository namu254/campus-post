"""change URL Configuration

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
from django.contrib import admin, auth
from django.urls import path, include
from changeapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sign_up', views.signUp, name='sign_up'),
    path('', views.index, name='index'),
    path('add_post', views.add_post, name='add_post'),
    path('add_comment', views.add_comment, name='add_comment'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('edit_interests', views.edit_interests, name='edit_interests'),
    path('get_interests', views.get_interests, name='get_interests'),
    path('submit_interest', views.submit_interest, name='submit_interest'),
    path('my_posts', views.my_posts, name='my_posts'),
    path('add_interest', views.add_interest, name='add_interest'),
    path('delete_post/<uuid:post_id>', views.delete_post, name='delete_post'),
    path('remove_account', views.remove_account, name='remove_account'),
    path('change_password', views.change_password, name='change_password'),
    path('interest/<str:interest>', views.interest, name='interest'),
    path('post_detail/<uuid:post_id>', views.post_detail, name='post_detail'),
    path('like/<uuid:post_id>', views.like, name='like'),
    path('flag_post/<uuid:post_id>', views.flag_post, name='flag_post'),
    path('check_like/<uuid:post_id>', views.check_like, name='check_like'),
    
    # # change password urls
    # path('password-change/', 'django.contrib.auth.views.password_change', name='password_change'),
    # path('password-change/done/', 'django.contrib.auth.views.password_change_done', name='password_change_done')

]
