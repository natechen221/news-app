from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponseBadRequest,QueryDict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from .models import *
from .forms import *
import time

#register
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        profile_form = UserProfileForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            profile_form = UserProfileForm(request.POST)
            if form.is_valid() and profile_form.is_valid():
                user = form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                username = form.cleaned_data.get('username')
                send_mail(
                    'Thank you for registering', #subject line
                    'Welcome to NewsWeb! We are looking forward to seeing you there and pelase free to comment on articles.', #actual message in email
                    settings.EMAIL_HOST_USER,
                    ['teamtencw3@gmail.com'],
                    fail_silently=False,
                )
                return redirect('login')
    context={'form':form, 'profile_form':profile_form}
    return render(request, 'myNews/register.html', context)

#login
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR password is incorrect')
    context={}
    return render(request, 'myNews/login.html', context)

#logout
def logoutUser(request):
    logout(request)
    return redirect('login')

#main page
@login_required(login_url='login')
def index(request):
    Articles = Article.objects.all()
    Category = ArticleCategory.objects.all()
    return render(request,'myNews/index.html',{
        'date':time.strftime("%Y-%m-%d", time.localtime()),
        'articles':Articles,
        'categories':Category,
        'user':request.user,
    })

#news page
@login_required(login_url='login')
def news(request,article_id):
    try:
        instance = get_object_or_404(Article,pk=article_id)
        initial_data = {
            "content_type": instance.get_content_type,
            "object_id": instance.id
        }
        article = Article.objects.get(id=article_id)
        comments = Comment.objects.filter_by_instance(instance)
        return render(request,'myNews/news.html',{
            'user':request.user,
            'article':article,
            'date':time.strftime("%Y-%m-%d", time.localtime()),
            'comments':comments,
            'comment_form':CommentForm(initial=initial_data),
        })
    except article.DoesNotExist:
        return HttpResponseBadRequest('Invalid article id')

#profile page
@login_required(login_url='login')
def profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'myNews/profile.html', args)

#edit page
@login_required(login_url='login')
def editprofile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.userprofile)
        pic_form = UpdateProfilePicture(request.POST,request.FILES,instance=request.user.userprofile)
        if form.is_valid() and pic_form.is_valid():
            form.save()
            pic_form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user.userprofile)
        pic_form = UpdateProfilePicture(instance=request.user.userprofile)
    args = {'form': form, 'pic_form':pic_form}
    return render(request, 'myNews/edit_profile.html', args)

@login_required(login_url='login')
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        else:
            return redirect('myNews/change_password.html')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'myNews/change_password.html', args)

# post comment
def post(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        content = request.POST['content']
        object_id = request.POST['object_id']
        content_type = ContentType.objects.get(model='article')
        comment = Comment(
            user = request.user,
            content_type = content_type,
            object_id = object_id,
            content = content,
        )
        comment.save()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})

# reply comment
def reply(request):
    if request.method == 'POST':
        content_type = ContentType.objects.get(model='article')
        obj_id = request.POST["object_id"]
        content = request.POST["content"]
        parent_obj = None
        try:
            parent_id = request.POST["parent_id"]
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id = parent_id)
            if parent_qs.exists() and parent_qs.count() ==1 :
                parent_obj = parent_qs.first()
        reply = Comment(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content,
            parent = parent_obj
        )
        reply.save()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})

# edit comment
def edit_comment(request):
    if request.method == 'PUT':
        data = QueryDict(request.body)
        comment_id = data['comment_id']
        content = data['content']
        if comment_id != None:
            comment = Comment.objects.get(pk=comment_id)
            comment.content = content
            comment.save()
            print( comment.content)
            return JsonResponse({'status':1})
        else:
            return JsonResponse({'status':0})

# delete comment
def delete(request):
    if request.method == 'DELETE':
        data = QueryDict(request.body)
        comment_id = data['comment_id']
        if comment_id != None:
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
            return JsonResponse({'status':1})
        else:
            return JsonResponse({'status':0})

#like article
def like_article(request):
    user = request.user
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article_obj = Article.objects.get(id = article_id)
        if user in article_obj.liked.all():
            article_obj.liked.remove(user)
        else:
            article_obj.liked.add(user)
        like, created = Like.objects.get_or_create(user=user,article=article_obj)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.vale = 'Like'
        like.save()
    return JsonResponse({'status':1})
