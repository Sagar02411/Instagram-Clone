from django.urls import path
from . import views

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='testindex'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin', views.SigninView.as_view(), name='signin'),
    path('search', views.UserSearchView.as_view(), name='search'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('profile/<str:pk>', views.ProfileView.as_view(), name='profile'),
    path('like-post', views.LikePostView.as_view(), name='like-post'),
    path('settings', views.SettingsVew.as_view(), name='settings'),
    path('follow', views.FollowView.as_view(), name='follow'),
    path('comment', views.CommentView.as_view(), name='comment'),
    path('commentreply', views.CommentReplyView.as_view(), name='comment'),
    path('comment/delete/<int:comment_id>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/edit/<int:comment_id>/', views.CommentEditView.as_view(), name='comment-edit'),
    path('username-valid', views.ValidUsernameView.as_view(), name='username-valid'),
    path('email-valid', views.ValidEmailView.as_view(), name='email-valid'),
    path('chat/', views.messages_view, name='chat'),
    path('toggle', views.toggleView.as_view(), name='toggle'),
    path('accept', views.AcceptPendigRequests.as_view(), name='accept'),
]