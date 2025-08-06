from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import MotdMessage


@login_required
def dashboard_widget(request):
    """Render the MOTD dashboard widget"""
    user = request.user
    active_messages = [
        message
        for message in MotdMessage.objects.filter(is_active=True)
        if message.can_user_see(user)
    ]

    priority_order = {'critical': 4, 'high': 3, 'normal': 2, 'low': 1}
    active_messages.sort(key=lambda x: priority_order.get(x.priority, 0), reverse=True)
    context = {
        'messages': active_messages[:5],
        'user': user,
    }
    return render(request, 'motd/dashboard_widget.html', context)
@login_required
def motd_list(request):
    user = request.user
    all_messages = [
        message
        for message in MotdMessage.objects.filter(is_active=True)
        if message.can_user_see(user)
    ]

    context = {
        'messages': all_messages,
        'user': user,
    }
    return render(request, 'motd/motd_list.html', context)
