from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .google_sheet import get_role
@login_required
def auth_router(request):
    email = request.user.email.lower()
    role = get_role(email)
    if role == "oc":
        if not request.user.is_staff:
            request.user.is_staff = True
            request.user.save(update_fields=["is_staff"])
        return redirect("admin_panel")
    if role == "team":
        return redirect("participant_dashboard")
    return redirect("access_denied")