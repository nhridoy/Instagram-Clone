from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from profile_app.forms import RegistrationForm, LoginForm, ChangeProfilePicForm, EditProfileForm, EditBasicForm
from profile_app.models import UserDetails, Follow
from post_app.models import Likes, Posts, Comments, SavedPost
from post_app.forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from django.contrib.auth.models import User
from django.core.paginator import Paginator


# Create your views here.
def login_executed(redirect_to):
    """This Decorator kicks authenticated user out of a view"""

    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


@login_executed('post_app:index')
def loginview(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        username, password = request.POST.get('username'), request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('post_app:index'))
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


@login_executed('post_app:index')
def registerview(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            userdetails = UserDetails.objects.create(user=user)
            login(request, user)
            return HttpResponseRedirect(reverse('post_app:index'))

    context = {
        'form': form
    }
    return render(request, 'login.html', context)


@login_required
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('post_app:index'))


@login_required
def UserProfileView(request):
    current_user = request.user
    form = ChangeProfilePicForm(instance=current_user.user_details)
    posts = Posts.objects.filter(user=request.user)
    liked_post = Likes.objects.filter(user=current_user)
    saved_post = SavedPost.objects.filter(user=request.user)
    follow_list = Follow.objects.filter(follower=request.user)
    follow_list2 = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    following_list = Follow.objects.filter(following=request.user)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        if 'upload_btn' in request.POST:
            form = ChangeProfilePicForm(request.POST, request.FILES, instance=current_user.user_details)
            if form.is_valid():
                user_obj = form.save(commit=False)
                user_obj.user = current_user
                user_obj.save()
                return HttpResponseRedirect(reverse('profile_app:profile'))
        elif 'comment_btn' in request.POST:
            user_comment = request.POST.get('user_comment')
            current_post_slug = request.POST.get('current_post')
            current_post = Posts.objects.get(slug=current_post_slug)
            comment_model = Comments()
            comment_model.user = current_user
            comment_model.post = current_post
            comment_model.comment = user_comment
            comment_model.save()
            return redirect(request.META['HTTP_REFERER'])

    context = {
        'form': form,
        'liked_post': liked_post.values_list('post', flat=True),
        'saved_post': saved_post.values_list('post', flat=True),
        'posts': posts,
        'follow_list': follow_list,
        'follow_list2': follow_list2,
        'following_list': following_list,
        'page_obj': page_obj,
    }
    return render(request, 'profile.html', context)


@login_required
def editprofileview(request, user_name):
    current_user = request.user
    form1 = EditBasicForm(instance=current_user)
    form = EditProfileForm(instance=current_user.user_details)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=current_user.user_details)
        form1 = EditBasicForm(request.POST, instance=current_user)
        if form.is_valid() and form1.is_valid():
            form.save()
            form = EditProfileForm(instance=current_user.user_details)

            form1.save()
            form1 = EditBasicForm(instance=current_user)
            return HttpResponseRedirect(reverse('profile_app:profile'))
    context = {
        'form': form,
        'form1': form1,
    }
    return render(request, 'edit-profile.html', context)


@login_required
def passchangeview(request):
    current_user = request.user
    form = PasswordChangeForm(user=current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=current_user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile_app:profile'))
    context = {
        'form': form,
    }
    return render(request, 'edit-profile.html', context)


@login_required
def OtherUserProfileView(request, user_name):
    other_user = User.objects.get(username=user_name)
    user_post = Posts.objects.filter(user__username=user_name)
    liked_post = Likes.objects.filter(user=request.user)
    saved_post = SavedPost.objects.filter(user=request.user)
    follow_list = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    follow_list2 = Follow.objects.filter(follower=other_user)
    following_list = Follow.objects.filter(following=other_user)

    paginator = Paginator(user_post, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if other_user == request.user:
        return HttpResponseRedirect(reverse('profile_app:profile'))
    else:
        if request.method == 'POST':
            if 'comment_btn' in request.POST:
                user_comment = request.POST.get('user_comment')
                current_post_slug = request.POST.get('current_post')
                current_post = Posts.objects.get(slug=current_post_slug)
                comment_model = Comments()
                comment_model.user = request.user
                comment_model.post = current_post
                comment_model.comment = user_comment
                comment_model.save()
                return redirect(request.META['HTTP_REFERER'])

    context = {
        'liked_post': liked_post.values_list('post', flat=True),
        'saved_post': saved_post.values_list('post', flat=True),
        'other_user': other_user,
        'follow_list': follow_list,
        'follow_list2': follow_list2,
        'following_list': following_list,
        'page_obj': page_obj,
    }
    return render(request, 'user.html', context)


@login_required
def userfollowview(request, user_name):
    current_user = request.user
    followed_user = User.objects.get(username=user_name)
    is_follow = Follow.objects.filter(follower=current_user, following=followed_user)

    if not is_follow:
        follow = Follow(follower=current_user, following=followed_user)
        follow.save()
        return redirect(request.META['HTTP_REFERER'])
    else:
        is_follow.delete()
        return redirect(request.META['HTTP_REFERER'])


@login_required
def searchview(request):
    all_users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    follow_list = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

    paginator = Paginator(all_users, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'GET':
        search_text = request.GET.get('search', '')
        search_result = User.objects.filter(username__icontains=search_text, is_superuser=False) \
                        | User.objects.filter(first_name__icontains=search_text, is_superuser=False)

        paginator = Paginator(search_result, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'all_users': all_users,
        'follow_list': follow_list,
        'page_obj': page_obj,
        'search_result': search_result,
        'search_text': search_text,
    }
    return render(request, 'search.html', context)
