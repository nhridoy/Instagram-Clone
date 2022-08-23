from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from post_app.models import Posts, Likes, Comments, SavedPost
from post_app.forms import PostForm, CommentForm, EditPostForm
from profile_app.models import UserDetails, User, Follow
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse_lazy
import uuid


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
# class IndexView(LoginRequiredMixin, ListView):
#     template_name = 'home.html'
#     paginate_by = 2
#
#     def get_context_data(self, **kwargs):
#         context = super(IndexView, self).get_context_data(**kwargs)
#         context['title'] = 'Home . Instagram'
#         return context


@login_required
def IndexView(request):
    all_users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    follow_li = Follow.objects.filter(follower=request.user).values_list('following')
    follow_list = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

    posts = Posts.objects.filter(user__in=follow_list)
    liked_post = Likes.objects.filter(user=request.user)
    saved_post = SavedPost.objects.filter(user=request.user)

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST' and 'comment_btn' in request.POST:
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
        'title': 'Home . Instagram',
        'all_user': all_users,
        'follow_list': follow_list,
        'posts': posts,
        'liked_post': liked_post.values_list('post', flat=True),
        'saved_post': saved_post.values_list('post', flat=True),
        'page_obj': page_obj,
    }
    return render(request, 'home.html', context)


@login_required
def postsaveview(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.slug = str(request.user) + str(uuid.uuid4())
            user_obj.save()
            return HttpResponseRedirect(reverse('profile_app:profile'))


@login_required
def likeview(request, slug_name):
    current_user = request.user
    current_post = Posts.objects.get(slug=slug_name)
    if is_liked := Likes.objects.filter(post=current_post, user=current_user):
        is_liked.delete()
    else:
        like_post = Likes(user=current_user, post=current_post)
        like_post.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def saveview(request, slug_name):
    current_user = request.user
    current_post = Posts.objects.get(slug=slug_name)
    if is_save := SavedPost.objects.filter(
        post=current_post, user=current_user
    ):
        is_save.delete()
    else:
        save_post = SavedPost(user=current_user, post=current_post)
        save_post.save()
    return redirect(request.META['HTTP_REFERER'])

# class EditPostView(LoginRequiredMixin, UpdateView):
#     # form_class = PostForm
#     model = Posts
#     fields = ('post_pic', 'post_caption',)
#     slug_url_kwarg = 'slug_name'
#     template_name = 'edit-post.html'
#     success_url = reverse_lazy('profile_app:profile')
#
#     def get_context_data(self, **kwargs):
#         context = super(EditPostView, self).get_context_data(**kwargs)
#         context['title'] = 'Home . Instagram'
#         # context['post_user'] = Posts.objects.get(slug=self.slug_url_kwarg)
#         context['post_user'] = self.slug_url_kwarg
#         return context

@login_required
def EditPostView(request, slug_name):
    current_post = Posts.objects.get(slug=slug_name)
    form = EditPostForm(instance=current_post)

    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=current_post)
        if form.is_valid():
            # form = EditPostForm(request.POST, request.FILES, instance=current_post)
            form.save()
            return HttpResponseRedirect(reverse('profile_app:profile'))
    context = {
        'form': form,
        'current_post': current_post,

    }
    return render(request, 'edit-post.html', context)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Posts
    slug_url_kwarg = 'slug_name'

    # success_url = reverse_lazy('profile_app:profile')

    def get_success_url(self):
        return reverse('profile_app:profile')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


# class PostView(LoginRequiredMixin, DetailView):
#     model = Posts
#     slug_url_kwarg = 'slug_name'
#     template_name = 'post.html'
#
#     # def get_queryset(self):
#     #     liked_post = Likes.objects.filter(user=self.request.user)
#     #
#     #     return liked_post

@login_required
def PostView(request, slug_name):
    current_user = request.user
    posts = Posts.objects.get(slug=slug_name)
    liked_post = Likes.objects.filter(user=current_user)
    saved_post = SavedPost.objects.filter(user=request.user)
    if request.method == 'POST':
        user_comment = request.POST.get('user_comment')
        comment_model = Comments()
        comment_model.user = current_user
        comment_model.post = posts
        comment_model.comment = user_comment
        comment_model.save()
        return redirect(request.META['HTTP_REFERER'])
    context = {
        'posts': posts,
        'liked_post': liked_post.values_list('post', flat=True),
        'saved_post': saved_post.values_list('post', flat=True),
    }
    return render(request, 'post.html', context)
