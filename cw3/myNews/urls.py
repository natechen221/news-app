from django.urls import path
from myNews import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/',views.logoutUser, name = 'logout'),
    path('', views.index, name='index'),
    path('news/<int:article_id>/', views.news, name='news'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/',views.editprofile, name = 'editprofile'),
    path('password/',views.changePassword, name = 'changepassword'),
    path('post_comment/',views.post, name = 'post_comment'),
    path('reply_comment/',views.reply, name = 'reply_comment'),
    path('delete_comment/',views.delete, name = 'delete_comment'),
    path('edit_comment/',views.edit_comment, name = 'edit_comment'),
    path('like/',views.like_article, name = 'like_article'),
]
