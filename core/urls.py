from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('signin', views.SigninView.as_view(), name='signin'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('profile/<str:pk>', views.ProfileView.as_view(), name='profile'),
    path('like-post', views.LikePostView.as_view(), name='like-post'),
    path('settings', views.SettingsVew.as_view(), name='settings'),
    path('follow', views.FollowView.as_view(), name='follow'),
    path('inbox', views.InboxView.as_view(), name='inbox'),
    path('direct/<username>', views.DirectsView.as_view(), name="directs"),
    path('send/', views.SendDirectView.as_view(), name="send-directs")
]