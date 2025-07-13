from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse


@login_required
def motd_dashboard(request: HttpRequest) -> HttpResponse:
    groups = request.user.groups.all()
    for group in groups:
        if group.name == "Capital Group":
            return HttpResponse(
                render_to_string("madashboard/motd.html", request=request)
            )
    return HttpResponse(
        render_to_string("madashboard/normal.html", request=request)
    )
