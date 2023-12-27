from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount
from itertools import chain
from django.views import View

class IndexView(View):
    def get(self, request):
        user_object = User.objects.get(username=request.user.username)

        feed = []
        feed_list = list(chain(*feed))

        all_users = User.objects.all()
        user_following_all = []

        return render(request, 'index.html', {'posts':feed_list})
    
    def post(self, request):
        print("try")
        return redirect('/')

class SignupView(View):
    def get(self, request):
        print("try")
        return render(request, 'signup.html')

    def post(self, request):
        print("hello")
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
    
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                print("signup successful !!")
                #create a Profile object for the new user
                # user_model = User.objects.get(username=username)
                # new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                # new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
class SigninView(View):
    def get(self, request):
        print("try")
        return render(request, 'signin.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return 
            ('signin')

class LogoutView(View):
    def get(self, request):
        print("try")
        return render(request, 'signup.html')

    def post(self, request):
        auth.logout(request)
        return redirect('signin')


class UploadView(View):
    @login_required(login_url='signin')
    def get(self, request):
        print("Upload post")
        return redirect('signin')

    def post(self, request):
        user = request.user.username
        image = request.FILES.get('image_upload')
        print("*"*20, image)

        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')

class LikePostView(View):
    @login_required(login_url='signin')
    def get(self, request):
        print("Like post")
        return redirect('/')
    
    def post(self, request):
        username = request.user.username
        post_id = request.GET.get('post_id')

        post = Post.objects.get(id=post_id)

        like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

        if like_filter == None:
            new_like = LikePost.objects.create(post_id=post_id, username=username)
            new_like.save()
            post.no_of_likes = post.no_of_likes+1
            post.save()
            return redirect('/')
        else:
            like_filter.delete()
            post.no_of_likes = post.no_of_likes-1
            post.save()
            return redirect('/')

class ProfileView(View):
    #@login_required(login_url='signin')
    def get(self, request, pk):
        
        user_object = User.objects.filter(username=pk).first()  # use filter insted of get Ref. from Mayur san
        print("profile")
        user_profile = Profile.objects.filter(user=user_object).first()
        user_posts = Post.objects.filter(user=pk)
        user_post_length = len(user_posts)

        follower = request.user.username
        user = pk
        print("*" * 20)
        for i in user_posts:
            print(i.image)

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            button_text = 'Unfollow'
        else:
            button_text = 'Follow'

        user_followers = len(FollowersCount.objects.filter(user=pk))
        user_following = len(FollowersCount.objects.filter(follower=pk))
        context = {
            'user_object': user_object,
            'user_profile': user_profile,
            'user_posts': user_posts,
            'user_post_length': user_post_length,
            'user_followers': user_followers,
            'user_following': user_following,
        }
        print(context)
        return render(request, 'profile.html', context)        

    def post(self, request, pk):
        print("profile view feature")
        return redirect('/')

class FollowView(View):
    @login_required(login_url='signin')
    def get(self, request):
        print("Follow feaure")
        return redirect('/')

    def post(self, request):
        print("Follow and unfolow feature")
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
