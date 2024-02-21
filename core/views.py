from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, Comment
from itertools import chain
from django.views import View
import random
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from asgiref.sync import sync_to_async
from .elasticsearch import search_users


class IndexView(View):
    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request):
        user_object = User.objects.filter(username=request.user.username).first()
        user_profile = Profile.objects.filter(user=user_object).first()
 
        user_following_list = [user.user for user in FollowersCount.objects.filter(follower=request.user.username)]
 
        # Fetch posts for the user's following list
        posts = Post.objects.filter(user__in=user_following_list)
        # Fetch comments for all posts
        comments_dict = {}
        for post1 in posts:
            comments = Comment.objects.filter(post=post1, active=True).order_by('-date')
            print('list of comments',comments)
            comments_list = []
            for obj in comments:
                if obj.parent is not None:
                    comments_list.append({'user': obj.user.username, 'comment': obj.comment, 'date': obj.date, 'cmt_id': obj.id, 'parent': obj.parent})
                else:
                    comments_list.append({'user': obj.user.username, 'comment': obj.comment, 'date': obj.date, 'cmt_id': obj.id})
            comments_dict[post1] = comments_list

        # print("line number 39",comments_dict)
        
        all_users = User.objects.all()
        user_following_all = [User.objects.get(username=user.user) for user in FollowersCount.objects.filter(follower=request.user.username)]
        new_suggestions_list = [user for user in all_users if user not in user_following_all]
        current_user = User.objects.filter(username=request.user.username)
        final_suggestions_list = [user for user in new_suggestions_list if user not in current_user]
 
        suggestions_username_profile_list = Profile.objects.filter(user__in=final_suggestions_list[:4])
 
        display_user = request.user.username 
        pending_follow_request = FollowersCount.objects.filter(user = request.user.username, status='pending')
        print(pending_follow_request)
        return render(request, 'testindex.html', {
            'user_profile': user_profile,
            'posts': posts,
            'suggestions_username_profile_list': suggestions_username_profile_list,
            'user': display_user,
            'comments_dict': comments_dict,
            'pending_follow_request': pending_follow_request,
            'is_public': user_profile.is_public
        })
   
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

        if password.isspace():
            messages.info(request, 'Password should not contain only space')
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
                return redirect('/')
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
        print(user)
        if user == None:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
        else:
            auth.login(request, user)
            return redirect('/')

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

        hashtages = []

        for word in caption.split():
            if '#' in word:
                index = word.index('#')
                if index < len(word) - 1:
                    hashtages.append(word[index + 1:])
                    
        print(hashtages)
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')

class LikePostView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request):
        username = request.user.username
        post_id = request.GET.get('post_id')
        print(post_id)
        post = Post.objects.filter(id=post_id).first()

        like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

        Liked = 0

        if like_filter == None:
            new_like = LikePost.objects.create(post_id=post_id, username=username)
            new_like.save()
            post.no_of_likes = post.no_of_likes+1
            post.save()
            Liked = 1

        else:
            like_filter.delete()
            post.no_of_likes = post.no_of_likes-1
            post.save()
        likes = post.no_of_likes
        context = {
            'likes': likes,
            'Liked': Liked
        }
        return JsonResponse(context,safe=False)

    def post(self, request):
        print("Like post")
        return redirect('/')

class ProfileView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request, pk):
        
        user_object = User.objects.filter(username=pk).first()  
        if user_object is None:
            messages.info(request, 'User does not exist')
            return redirect('/')

        user_profile = Profile.objects.filter(user=user_object).first()
        user_posts = Post.objects.filter(user=pk)
        user_post_length = len(user_posts)

        follower = request.user.username
        user = pk

        if FollowersCount.objects.filter(follower=follower, user=user, status='accepted').first():
            button_text = 'Unfollow'
        elif FollowersCount.objects.filter(follower=follower, user=user, status='pending').first():
            button_text = 'Pending'
        else:
            button_text = 'Follow'
            print(button_text)

        user_followers = len(FollowersCount.objects.filter(user=pk, status = 'accepted'))
        user_following = len(FollowersCount.objects.filter(follower=pk, status='accepted'))
        is_public = FollowersCount.objects.filter(follower=follower, user=user, status='accepted').exists() or user_profile.is_public
        context = {
            'user_object': user_object,
            'user_profile': user_profile,
            'user_posts': user_posts,
            'button_text': button_text,
            'user_post_length': user_post_length,
            'user_followers': user_followers,
            'user_following': user_following,
            'is_public': is_public
        }
        return render(request, 'testprofile.html', context)        

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
        follower = request.POST['follower']
        user = request.POST['user']
        print("Follow and unfolow feature", follower, user)

        if FollowersCount.objects.filter(follower=follower, user=user, status='accepted').first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        elif FollowersCount.objects.filter(follower=follower, user=user, status='pending').first():
            messages.info(request, 'Follow request already sent')
            return redirect('/profile/'+user)
        else:
            user_object = User.objects.filter(username=user).first()
            follower_obj = Profile.objects.filter(user=user_object).first()
            if follower_obj.is_public:
                new_follower = FollowersCount.objects.create(follower=follower, user=user, status='accepted')
                new_follower.save()
                return redirect('/profile/'+user)
            else:
                follow_request = FollowersCount(follower=follower, user=user)
                follow_request.save()
                messages.success(request, 'Follow request sent successfully')
                return redirect('/profile/'+user)
        
class SettingsVew(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)
        context = {
            'user_profile': user_profile,
            'is_public': user_profile.is_public
        }
        return render(request, 'setting.html', context)

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
        
        context={
            "is_public": user_profile.is_public
        }

        return render('settings', context)

class CommentView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def post(self, request):
        post_id = request.POST.get('post_id')
        comment_text = request.POST.get('comment')

        if comment_text.isspace():
            messages.info(request, 'Comment should not contain the only space', extra_tags='comment')
            return redirect('/')

        if post_id and comment_text:
            post = Post.objects.get(pk=post_id)
            Comment.objects.create(post=post, user=request.user, comment=comment_text)

        return redirect('/')

class CommentDeleteView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)

        comment.soft_delete()

        return redirect('/')

class CommentEditView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        print("*"*50, request.POST.get('comment'))
        comment_text = request.POST.get('commentedit')
        
        if comment_text.isspace():
            messages.info(request, 'Comment should not contain the only space', extra_tags='comment')
            return redirect('/')

        comment.comment = comment_text
        comment.save()
        return redirect('/')

class CommentReplyView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        comment_text = request.POST.get('commentreply')
        parent_id = request.POST.get('parent_id')
        parent = Comment.objects.get(id=parent_id)

        if comment_text.isspace():
            messages.info(request, 'Comment should not contain the only space', extra_tags='comment')
            return redirect('/')

        if post_id and comment_text:
            post = Post.objects.get(pk=post_id)
            Comment.objects.create(post=post, user=request.user, comment=comment_text, parent=parent)

        return redirect('/')

class UserSearchView(View):
    @method_decorator(login_required(login_url='signin'), name='signin')
    def post(self, request):
        username = request.POST['search_query']
        if username.isspace():
            messages.info(request, 'Username should not contain the only space', extra_tags='search')
            return redirect('/')
        username_object = User.objects.filter(username__startswith=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))

        user_object = User.objects.filter(username=request.user.username).first()
        user_profile = Profile.objects.filter(user=user_object).first()
        return render(request, 'testsearch.html', {'username_profile_list': username_profile_list, 'user_profile': user_profile})

class ValidUsernameView(View):
    def post(self, request):
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            return JsonResponse('Username already taken!!', safe=False)
        
        if username.islower() == False:
            return JsonResponse('Username must be in lower case!!', safe=False)

        return JsonResponse('', safe=False)

class ValidEmailView(View):
    def post(self, request):
        email = request.POST['email']
        print(email)
        if User.objects.filter(email=email).exists():
            return JsonResponse('email already taken', safe=False)


        return JsonResponse('', safe=False)

def messages_view(request):
    all_users = User.objects.all()    
    return render(request, 'testmessages.html', {'all_users': all_users})

class toggleView(View):
    def post(self, request):
        user_object = User.objects.filter(username=request.user.username).first()
        user_obj = Profile.objects.filter(user=user_object).first()
        user_obj.is_public = not request.POST['is_public'] == 'true'
        user_obj.save()
        return HttpResponse('success')

class AcceptPendigRequests(View):
    def post(self, request):
        follower = request.POST['follower']
        user = request.POST['user']

        print("*"*25,follower, user)

        follow_obj = FollowersCount.objects.filter(follower=user, user=follower).first()
        print(follow_obj)
        follow_obj.status = 'accepted'
        follow_obj.save()

        return redirect('/')