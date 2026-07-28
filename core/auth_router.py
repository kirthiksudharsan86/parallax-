from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .google_sheet import get_role


@login_required
def auth_router(request):
    role = get_role(request.user.email.lower())

    if role == "oc":
        return redirect("admin_panel")

    if role == "team":
        return redirect("participant_dashboard")

    return redirect("access_denied")