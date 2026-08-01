from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .google_sheet import get_participant
from .models import Participant, Team
@login_required
def auth_router(request):
    email = request.user.email.lower()
    data = get_participant(email)
    if data is None:
        return redirect("access_denied")
    if data["role"] == "oc":
        if not request.user.is_staff:
            request.user.is_staff = True
            request.user.save(update_fields=["is_staff"])
        return redirect("admin_panel")
    team_name = data.get("Team Name", "").strip()
    team = Team.objects.filter(team_name__iexact=team_name).first()
    if team is None:
        team = Team.objects.create(
        team_name=team_name,
        team_code=Team.generate_unique_team_code(),
    )
    participant = Participant.objects.filter(email__iexact=email).first()
    if participant is None:
        participant = Participant.objects.create(
            user=request.user,
            full_name=data.get("Lead", ""),
            email=email,
            phone_number=data.get("Phone Number", ""),
            college_name=data.get("College Name", ""),
            team=team,
            is_team_leader=True,
        )
        team.leader = participant
        team.save(update_fields=["leader"])
    else:
        if participant.user != request.user:
            participant.user = request.user
        participant.team = team
        participant.is_team_leader = True
        participant.save(update_fields=["user", "team", "is_team_leader"])
    return redirect("participant_dashboard")