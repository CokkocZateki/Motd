from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import GroupMotd, StateMotd


@login_required
def motd_dashboard(request: HttpRequest) -> HttpResponse:
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
