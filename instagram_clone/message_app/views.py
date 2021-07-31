from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from message_app.models import Messaging
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count


# Create your views here.

@login_required
def inboxview(request):
    message_list = Messaging.objects.filter(sender=request.user).distinct() | \
                   Messaging.objects.filter(receiver=request.user).distinct()


    print(message_list.query)
    paginator = Paginator(message_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # print(message_list.query)
    context = {
        'message_list': message_list,
        'page_obj': page_obj,
    }

    return render(request, 'inbox.html', context)


@login_required
def messageview(request, user_name):
    sender_user = request.user
    receiver_user = User.objects.get(username=user_name)
    message_list = Messaging.objects.filter(sender=sender_user, receiver=receiver_user).order_by('message_date') | \
                   Messaging.objects.filter(receiver=sender_user, sender=receiver_user).order_by('message_date')



    if request.method == 'POST':
        msg_text = request.POST.get('msg_text')
        messaging = Messaging()
        messaging.sender = sender_user
        messaging.receiver = receiver_user
        messaging.message_text = msg_text
        messaging.save()

        return redirect(request.META['HTTP_REFERER'])

    context = {
        'sender_user': sender_user,
        'receiver_user': receiver_user,
        'message_list': message_list,
    }
    return render(request, 'message.html', context)
