from django import forms
from post_app.models import Posts, Comments


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ('user', 'slug',)


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'text-comment', 'placeholder': 'Add a Comment...', 'style': 'width: auto;',
               'id': 'post-{{ posts.slug }}'}))

    class Meta:
        model = Comments
        fields = ('comment',)


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ('user', 'slug',)
