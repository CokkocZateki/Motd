# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Motd
from motd import __title__
from motd.forms import MotdMessageForm
from motd.models import MotdMessage

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@login_required
@permission_required("motd.basic_access")
def dashboard_widget(request: WSGIRequest):
    """Render the MOTD dashboard widget"""
    active_messages = MotdMessage.objects.visible_to(request.user).filter(
        is_active=True
    )[:5]
    context = {
        "messages": active_messages,
    }
    return render(request, "motd/dashboard_widget.html", context)


@login_required
@permission_required("motd.basic_access")
def motd_list(request: WSGIRequest):
    all_messages = MotdMessage.objects.visible_to(request.user).filter(is_active=True)
    expired_messages = MotdMessage.objects.visible_to(request.user).filter(
        is_active=False
    )[:10]
    context = {
        "active_messages": all_messages,
        "expired_messages": expired_messages,
    }
    return render(request, "motd/motd_list.html", context)


@login_required
@permission_required("motd.manage_access")
def motd_create(request: WSGIRequest):
    """Create a new MOTD message"""
    if request.method == "POST":
        form = MotdMessageForm(request.POST)
        if form.is_valid():
            motd = form.save(commit=False)
            motd.created_by = request.user
            motd.save()
            form.save_m2m()  # Save many-to-many relationships

            messages.success(request, "Message created successfully.")
            return redirect("motd:list")
    else:
        form = MotdMessageForm()

    return render(request, "motd/motd_form.html", {"form": form, "action": "Create"})


@login_required
@permission_required("motd.manage_access")
def motd_edit(request: WSGIRequest, pk):
    """Edit an existing MOTD message"""
    motd_message = get_object_or_404(MotdMessage, pk=pk)

    if request.method == "POST":
        form = MotdMessageForm(request.POST, instance=motd_message)
        if form.is_valid():
            form.save()

            messages.success(request, "Message updated successfully.")
            return redirect("motd:list")
    else:
        form = MotdMessageForm(instance=motd_message)

    return render(request, "motd/motd_form.html", {"form": form, "action": "Edit"})


@login_required
@permission_required("motd.manage_access")
def motd_delete(request: WSGIRequest, pk: int):
    """Delete a MOTD message"""
    motd_message = get_object_or_404(MotdMessage, pk=pk)

    if request.method == "POST":
        motd_message.delete()
        msg = _(f"Message {motd_message.title} deleted successfully.")
        messages.success(request, msg)
        return JsonResponse(
            data={"message": msg, "success": True}, status=200, safe=False
        )

    msg = _("You are not allowed to delete this message.")
    return JsonResponse(data={"message": msg, "success": False}, status=404, safe=False)
