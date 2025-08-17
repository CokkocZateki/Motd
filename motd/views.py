import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .forms import MotdMessageForm
from .models import MotdMessage, GroupMotd, StateMotd

logger = logging.getLogger(__name__)


@login_required
def dashboard_widget(request):
    """Render the MOTD dashboard widget"""
    user = request.user
    logger.info(f"User {user.username} loading dashboard widget")
    
    # Get all active messages for debugging
    all_active = MotdMessage.objects.filter(is_active=True).order_by('-start_date')
    logger.info(f"Dashboard widget: Found {all_active.count()} active messages")
    
    active_messages = []
    for message in all_active:
        can_see = message.can_user_see(user)
        logger.info(f"Dashboard widget - Message '{message.title}': can_user_see = {can_see}, show_to_all = {message.show_to_all}, restricted_groups = {list(message.restricted_to_groups.values_list('name', flat=True))}")
        if can_see:
            active_messages.append(message)

    logger.info(f"Dashboard widget: User can see {len(active_messages)} messages")

    context = {
        'messages': active_messages[:5],
        'user': user,
        'can_add_message': request.user.has_perm('motd.add_motdmessage'),
    }
    return render(request, 'motd/dashboard_widget.html', context)


@login_required
def motd_list(request):
    user = request.user
    logger.info(f"User {user.username} viewing MOTD list")
    
    # Log user's groups and state for debugging
    user_groups = list(user.groups.values_list('name', flat=True))
    logger.info(f"User groups: {user_groups}")
    
    if hasattr(user, 'profile') and hasattr(user.profile, 'state'):
        user_state = user.profile.state.name if user.profile.state else 'No state'
        logger.info(f"User state: {user_state}")
    else:
        logger.info("User has no profile/state")
    
    # Get all active messages for debugging
    all_active = MotdMessage.objects.filter(is_active=True).order_by('-start_date')
    logger.info(f"Found {all_active.count()} active messages")
    
    all_messages = []
    for message in all_active:
        can_see = message.can_user_see(user)
        restricted_groups = list(message.restricted_to_groups.values_list('name', flat=True))
        logger.info(f"Message '{message.title}': can_user_see = {can_see}, show_to_all = {message.show_to_all}, restricted_groups = {restricted_groups}")
        if can_see:
            all_messages.append(message)

    logger.info(f"User can see {len(all_messages)} messages total")

    context = {
        'messages_list': all_messages,
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
            message.save()  # Save the message first
            
            # Now save the many-to-many relationships
            form.save_m2m()
            
            # Debug: Check if groups were saved
            logger.info(f"Message '{message.title}' saved with {message.restricted_to_groups.count()} groups")
            
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
            message = form.save(commit=False)
            message.save()  # Save the message first
            
            # Now save the many-to-many relationships
            form.save_m2m()
            
            logger.info(f"Message '{message.title}' updated with {message.restricted_to_groups.count()} groups")
            
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
        logger.info(f"Deleting message '{motd_message.title}' by user {request.user.username}")
        motd_message.delete()
        messages.success(request, f'Message "{motd_message.title}" deleted successfully.')
        return redirect('motd:list')
    
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
