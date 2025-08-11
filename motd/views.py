from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render

from .forms import MotdMessageForm
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


@permission_required('motd.add_motdmessage')
def motd_create(request):
    """Create a new MOTD message from the dashboard"""
    if request.method == 'POST':
        form = MotdMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.created_by = request.user
            message.save()
            form.save_m2m()
            messages.success(request, 'Message created successfully.')
            return redirect('motd:list')
    else:
        form = MotdMessageForm()

    return render(request, 'motd/motd_form.html', {'form': form})
