from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, Message, Comment
from itertools import chain
from django.views import View
import random
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




class IndexView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request):
        user_object = User.objects.filter(username=request.user.username).first()
        print("*" * 50, user_object.username)
        user_profile = Profile.objects.filter(user=user_object).first()

        feed = []
        user_following_list = []

        user_following = FollowersCount.objects.filter(follower=request.user.username)

        for users in user_following:
            user_following_list.append(users.user)

        for usernames in user_following_list:
            feed_lists = Post.objects.filter(user=usernames)
            feed.append(feed_lists)

        feed_list = list(chain(*feed))
        all_users = User.objects.all()
        user_following_all = []

        for user in user_following:
            user_list = User.objects.get(username=user.user)
            user_following_all.append(user_list)
        
        new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
        current_user = User.objects.filter(username=request.user.username)
        final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
        random.shuffle(final_suggestions_list)

        username_profile = []
        username_profile_list = []

        for users in final_suggestions_list:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        suggestions_username_profile_list = list(chain(*username_profile_list))

        post = Post.objects.all()
        #print("*"*50, user_following)
        display_user = request.user.username
        return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4], 'user': display_user})
    
    def post(self, request):
        #print("try")
        return redirect('/')

class SignupView(View):
    def get(self, request):
        #print("try")
        return render(request, 'signup.html')

    def post(self, request):
        #print("hello")
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
    
        try:
            validate_password(password, user=User)
        except ValidationError as e:
            messages.info(request, ' '.join(e))
            return redirect('signup')

        if username.lower() in password.lower():
            messages.info(request, 'Password should not contain the username')
            return redirect('signup')
        
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
                # create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
class SigninView(View):
    def get(self, request):
        #print("try")
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
        auth.logout(request)
        return redirect('signin')

    def post(self, request):
        return redirect('signin')


class UploadView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request):
        return redirect('signin')

    @method_decorator(login_required(login_url='signin'), name='signin')
    def post(self, request):
        user = request.user.username
        image = request.FILES.get('image_upload')
        # print("*"*20, image)

        if not image.content_type.startswith('image/'):
            return HttpResponseBadRequest("Only JPEG and PNG images are allowed.")

        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')

class LikePostView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request):
        post_id = request.GET.get('post_id')
        print(post_id)
        post = Post.objects.filter(id=post_id).first()

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

    def post(self, request):
        print("Like post")
        return redirect('/')

class ProfileView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request, pk):
        #print("*"*50)
        user_object = User.objects.filter(username=pk).first()  
        print(user_object)
        if user_object is None:
            messages.info(request, 'User does not exist')
            return redirect('/')

        user_profile = Profile.objects.filter(user=user_object).first()
        user_posts = Post.objects.filter(user=pk)
        user_post_length = len(user_posts)

        follower = request.user.username
        user = pk
        #print("*" * 20)
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
            'button_text': button_text,
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
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request):
        print("Follow feaure ")
        return redirect('/')

    @method_decorator(login_required(login_url='signin'), name='signin')
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
        
class SettingsVew(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)
        print("*" * 50, "Setting button")
        return render(request, 'setting.html', {'user_profile': user_profile})

    @method_decorator(login_required(login_url='signin'), name='signin')
    def post(self, request):
        user_profile = Profile.objects.get(user=request.user)
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            user_profile.profileimg = image
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            user_profile.profileimg = image
            user_profile.save()
        
        return redirect('settings')
    
class InboxView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request):
        print(request.user)
        messages = Message.objects.filter(recipient=request.user, is_read=False)
        print(messages)
        return render(request, 'inbox.html', {'messages': messages})

    @method_decorator(login_required(login_url='signin'), name='signin')
    def post(self, request):
        user = request.user
        messages = Message.objects.filter(recipient=user, is_read=False)
        # ... rest of your code ...
        pass

class SendMessageView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request, recipient_username):
        return render(request, 'send_message.html', {'recipient_username': recipient_username})

    @method_decorator(login_required(login_url='signin'), name='signin')
    def post(self, request, recipient_username):
        body = request.POST.get('body')
        recipient = User.objects.get(username=recipient_username)
        Message.objects.create(sender=request.user, recipient=recipient, body=body)
        return redirect('inbox')

class CommentView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def post(self, request):
        post_object = Post.objects.filter(id = request.post).first()
        user = request.user.username
        comment = request.POST.get('comment')
        new_comment = Comment.objects.create(post = post_object.post_id, user=user, comment=comment)
        new_comment.save()
        
        return redirect('/')
