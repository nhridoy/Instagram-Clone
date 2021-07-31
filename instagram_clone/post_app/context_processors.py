from post_app.forms import PostForm


def post_form(request):
    form = PostForm
    return {
        'post_form': form,
    }
