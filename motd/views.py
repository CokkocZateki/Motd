from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .forms import MotdMessageForm
from .models import MotdMessage, GroupMotd, StateMotd


@login_required
def dashboard_widget(request):
    """Render the MOTD dashboard widget"""
    user = request.user
    active_messages = [
        message
        for message in MotdMessage.objects.filter(is_active=True).order_by('-start_date')
        if message.can_user_see(user)
    ]

    context = {
        'messages': active_messages[:5],
        'user': user,
        'can_add_message': request.user.has_perm('motd.add_motdmessage'),
    }
    return render(request, 'motd/dashboard_widget.html', context)


@login_required
def motd_list(request):
    user = request.user
    all_messages = [
        message
        for message in MotdMessage.objects.filter(is_active=True).order_by('-start_date')
        if message.can_user_see(user)
    ]

    context = {
        'messages_list': all_messages,  # Changed from 'messages' to avoid conflict with Django messages
        'user': user,
    }
    return render(request, 'motd/motd_list.html', context)


@login_required
@permission_required('motd.add_motdmessage')
def motd_create(request):
    """Create a new MOTD message"""
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

    return render(request, 'motd/motd_form.html', {'form': form, 'action': 'Create'})


@login_required
@permission_required('motd.change_motdmessage')
def motd_edit(request, pk):
    """Edit an existing MOTD message"""
    motd_message = get_object_or_404(MotdMessage, pk=pk)
    
    if request.method == 'POST':
        form = MotdMessageForm(request.POST, instance=motd_message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message updated successfully.')
            return redirect('motd:list')
    else:
        form = MotdMessageForm(instance=motd_message)

    return render(request, 'motd/motd_form.html', {'form': form, 'action': 'Edit'})


@login_required
@permission_required('motd.delete_motdmessage')
def motd_delete(request, pk):
    """Delete a MOTD message"""
    motd_message = get_object_or_404(MotdMessage, pk=pk)
    
    if request.method == 'POST':
        motd_message.delete()
        messages.success(request, f'Message "{motd_message.title}" deleted successfully.')
        return redirect('motd:list')
    
    # If not POST, redirect to list
    return redirect('motd:list')


@login_required
def motd_dashboard(request: HttpRequest) -> HttpResponse:
    """Legacy group/state MOTD system"""
    user_groups = request.user.groups.all()
    group_motds = (
        GroupMotd.objects.filter(group__in=user_groups, enabled=True)
        .select_related("group")
        .order_by("group__name")
    )

    user_state = getattr(getattr(request.user, "profile", None), "state", None)
    if user_state:
        state_motds = StateMotd.objects.filter(
            state_name=getattr(user_state, "name", str(user_state)), enabled=True
        ).order_by("state_name")
    else:
        state_motds = StateMotd.objects.none()

    motds = list(state_motds) + list(group_motds)

    if motds:
        return render(request, "motd/motd.html", {"motds": motds})

    return render(request, "motd/normal.html")
