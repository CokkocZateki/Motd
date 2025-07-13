from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from .models import GroupMotd


@login_required
def motd_dashboard(request: HttpRequest) -> HttpResponse:
    user_groups = request.user.groups.all()
    motds = (
        GroupMotd.objects.filter(group__in=user_groups, enabled=True)
        .select_related("group")
        .order_by("group__name")
    )
    if motds:
        return HttpResponse(
            render_to_string(
                "madashboard/motd.html", {"motds": motds}, request=request
            )
        )
    return HttpResponse(
        render_to_string("madashboard/normal.html", request=request)
    )
