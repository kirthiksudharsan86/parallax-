from datetime import date
from decimal import Decimal, InvalidOperation
from django.shortcuts import render
from .google_sheet import get_role
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Prefetch, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from core.emailing import leader_payment_confirmation, leader_registration_received
from core.models import (
    Announcement,
    EventConfiguration,
    LeaderRegistration,
    Marks,
    Participant,
    ProblemStatement,
    Review,
    Sponsor,
    Team,
    Track,
)
REGISTRATION_FIELD_LABELS = {
    'first_name': 'first name',
    'last_name': 'last name',
    'email': 'email ID',
    'phone_number': 'phone number',
    'college': 'college',
    'department': 'department',
    'reg_number': 'registration number',
    'graduation_year': 'year',
    'team_name': 'team name',
    'team_members': 'team members',
}
DEFAULT_TRACKS = [
    {
        'name': 'Aviation & Space Tech',
        'description': 'Build intelligent systems for aerospace, autonomous flight and satellite technologies.',
        'icon': 'fa-rocket',
    },
    {
        'name': 'Internet of Things"',
        'description': 'Create real-time hardware-software systems for devices, automation and edge computing.',
        'icon': 'fa-microchip',
    },
    {
        'name': 'Healthcare & Assistive Tech',
        'description': 'Design technologies that improve access, rehabilitation and quality of life.',
        'icon': 'fa-heart-pulse',
    },
    {
        'name': 'Artificial Intelligence & Machine Learning',
        'description': 'Engineer resilient cities through smart energy, mobility and monitoring.',
        'icon': 'fa-robot',
    },
    {
        'name': 'Communication & Networking',
        'description': 'Develop secure networks and intelligent connected infrastructure.',
        'icon': 'fa-satellite-dish',
    },
]

TRACK_ICON_MAP = {
    'Artificial intelligence': 'fa-brain',
    'Machine learning': 'fa-robot',
    'healthcare': 'fa-heart-pulse',
    'iot': 'fa-microchip',
    'web': 'fa-globe',
    'robotics': 'fa-gears',
}

INFORMATION_PAGES = {
    'schedule': ('Review Schedule', 'Every checkpoint is designed to turn momentum into measurable progress.'),
    'prizes': ('Prizes & Recognition','  '),
    'guidelines': ('Guidelines', 'Build boldly. Work fairly. Leave every space better than you found it.'),
    'theme': ('Theme', 'Same problem. Different view. Better answer.'),
    'contact': ('Contact the OC', 'Have a question? The organising committee is here to help.'),
}


def home(request):
    published_tracks = list(
        Track.objects.filter(is_published=True).select_related('prize').annotate(team_total=Count('teams')).order_by('name')
    )
    reviews = Review.objects.all().order_by('scheduled_at')

    active_sponsors = list(Sponsor.objects.filter(is_active=True))
    context = {
        'stats': build_home_stats(reviews),
        'tracks': build_home_track_cards(published_tracks) if published_tracks else build_default_track_cards(),
        'title_sponsors': [s for s in active_sponsors if s.sponsor_type == Sponsor.TITLE],
        'technical_sponsors': [s for s in active_sponsors if s.sponsor_type == Sponsor.TECHNICAL],
        'announcements': Announcement.objects.all().order_by('-is_pinned', '-created_at')[:6],
    }
    return render(request, 'parallax/home.html', context)


def about(request):
    context = {
        'core_members': [],
    }
    return render(request, 'parallax/about.html', context)


def tracks(request):
    published_tracks = list(
        Track.objects.filter(is_published=True)
        .prefetch_related(
            Prefetch(
                'problem_statement_slots',
                queryset=ProblemStatement.objects.filter(is_published=True, is_active=True).order_by('code', 'title'),
                to_attr='public_problem_statements',
            )
        )
        .order_by('name')
    )
    context = {'tracks': published_tracks or build_default_track_cards()}
    return render(request, 'parallax/tracks.html', context)


def faq(request):
    return render(request, 'parallax/faq.html')


def information(request, page):
    if page not in INFORMATION_PAGES:
        raise Http404('Information page not found.')

    heading, tagline = INFORMATION_PAGES[page]
    context = {
        'page': page,
        'heading': heading,
        'tagline': tagline,
        'reviews': Review.objects.all().order_by('scheduled_at'),
        'tracks': build_default_track_cards(),
    }
    return render(request, 'parallax/information.html', context)


    if page not in pages:
        from django.http import Http404
        raise Http404("Page not found")


    if page not in pages:
        from django.http import Http404
        raise Http404("Page not found")

    return render(
        request,
        'parallax/information.html',
        {
            'page': page,
            'heading': pages[page][0],
            'tagline': pages[page][1],
            'reviews': Review.objects.all().order_by('scheduled_at'),
            'tracks': public_tracks(),
        }
    )
def team_dashboard_static(request):
    return render(request, 'parallax/team_dashboard_static.html')


def team_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_panel')

        participant = ensure_participant_record(request.user)
        if participant.team:
            return redirect('participant_dashboard')

    return render(request, 'parallax/team_login.html')
    return render(
        request,
        'parallax/team_login.html',
        {'google_login_enabled': getattr(settings, 'GOOGLE_OAUTH_CONFIGURED', False)},
    )



def registration_index(request):
    return render(request, 'parallax/registration/index.html')

def registration_event_hub(request):
    """Steps 3 & 4 - hand off to the external event hub and handle the return."""
    registration = _current_leader_registration(request)
    if registration is None:
        messages.info(request, 'Please complete the team leader registration first.')
        return redirect('registration_leader')

    # Step 4: the event hub redirects back with ?status=paid once payment is done.
    if request.GET.get('status') == 'paid':
        if registration.payment_status != LeaderRegistration.PAYMENT_PAID:
            registration.payment_status = LeaderRegistration.PAYMENT_PAID
            registration.save(update_fields=['payment_status', 'updated_at'])
        if not registration.payment_email_sent:
            leader_payment_confirmation(registration)  # placeholder - Akash owns real email
            registration.payment_email_sent = True
            registration.save(update_fields=['payment_email_sent', 'updated_at'])
        messages.success(request, 'Payment confirmed. Welcome to Parallax 2026!')
        return redirect('registration_payment')

    context = {
        'registration': registration,
        'event_hub_url': getattr(settings, 'EVENT_HUB_URL', '#'),
    }
    return render(request, 'parallax/registration/event_hub.html', context)

@login_required(login_url='team_login')
@login_required
def participant_dashboard(request):
    if request.user.is_staff:
        return redirect("admin_panel")

    role = get_role(request.user.email.lower())

    if role != "team":
        return redirect("access_denied")

    context = {
        "user": request.user,
        "email": request.user.email,
        "name": request.user.get_full_name() or request.user.username,
    }

    return render(request, "parallax/dashboard.html", context)
@login_required(login_url='team_login')
def admin_panel(request):
    if not request.user.is_staff:
        return redirect('home')

    configuration = EventConfiguration.get_solo()

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()

        if action == 'update_event_date':
            raw_date = request.POST.get('event_start_date', '').strip()
            if not raw_date:
                messages.error(request, 'Event start date is required.')
            else:
                try:
                    configuration.event_start_date = date.fromisoformat(raw_date)
                    configuration.save(update_fields=['event_start_date', 'updated_at'])
                    messages.success(request, 'Event start date updated successfully.')
                except ValueError:
                    messages.error(request, 'Enter a valid event start date.')
            return redirect('admin_panel')

        if action in {'toggle_set_one', 'toggle_set_two'}:
            release = request.POST.get('release') == 'true'
            set_number = 1 if action == 'toggle_set_one' else 2

            try:
                configuration.update_problem_set_release(set_number, release, current_time=timezone.now())
                configuration.save()
                state_label = 'released' if release else 'hidden'
                messages.success(request, f'Problem Statement Set {set_number} is now {state_label}.')
            except ValueError as error:
                messages.error(request, str(error))

            return redirect('admin_panel')

    track_summary = list(Track.objects.annotate(team_total=Count('teams')).order_by('-team_total', 'name'))
    most_chosen_track = next((track for track in track_summary if track.team_total), None)
    recent_teams = Team.objects.select_related('leader', 'track').annotate(participant_total=Count('members')).order_by(
        '-created_at'
    )[:8]

    total_leader_registrations = LeaderRegistration.objects.count()
    total_leaders_paid = LeaderRegistration.objects.filter(
        payment_status=LeaderRegistration.PAYMENT_PAID
    ).count()
    total_leaders_pay_later = LeaderRegistration.objects.filter(
        payment_status=LeaderRegistration.PAYMENT_PAY_LATER
    ).count()

    problem_statement_summary = list(
        ProblemStatement.objects.select_related('track')
        .annotate(booked_total=Count('booked_teams'))
        .order_by('track__name', 'code', 'title')
    )

    context = {
        'configuration': configuration,
        'pending_teams': Team.objects.filter(status='PENDING').count(),
        'approved_teams': Team.objects.filter(status='APPROVED').count(),
        'total_registered_participants': Participant.objects.filter(team__isnull=False).count(),
        'total_payment_confirmed_participants': Participant.objects.filter(team__payment_confirmed=True).count(),
        'total_registered_teams': Team.objects.count(),
        'total_payment_confirmed_teams': Team.objects.filter(payment_confirmed=True).count(),
        'total_leader_registrations': total_leader_registrations,
        'total_leaders_paid': total_leaders_paid,
        'total_leaders_pay_later': total_leaders_pay_later,
        'problem_statement_summary': problem_statement_summary,
        'most_chosen_track': most_chosen_track,
        'configuration': configuration,
        'track_summary': track_summary,
        'recent_teams': recent_teams,
    }
    return render(request, 'parallax/admin/dashboard.html', context)


@login_required(login_url='team_login')
def admin_teams(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        action = request.POST.get('action')
        team = get_object_or_404(Team, id=team_id)

        if action == 'approve':
            team.status = 'APPROVED'
            team.save(update_fields=['status', 'updated_at'])
            messages.success(request, f'{team.team_name} marked as approved.')
        elif action == 'reject':
            team.status = 'REJECTED'
            team.save(update_fields=['status', 'updated_at'])
            messages.success(request, f'{team.team_name} marked as rejected.')
        elif action == 'confirm_payment':
            team.payment_confirmed = True
            team.save()
            messages.success(request, f'Payment confirmed for {team.team_name}.')
        elif action == 'unconfirm_payment':
            team.payment_confirmed = False
            team.save()
            messages.success(request, f'Payment confirmation removed for {team.team_name}.')

        return redirect('admin_teams')

    teams = (
        Team.objects.select_related('leader', 'track')
        .prefetch_related('members__user')
        .annotate(participant_total=Count('members'))
        .order_by('-created_at')
    )
    context = {'teams': teams}

    selected_track_id = request.GET.get('track', '').strip()
    if selected_track_id:
        teams = teams.filter(track_id=selected_track_id)

    context = {
        'teams': teams,
        'tracks': Track.objects.order_by('name'),
        'selected_track_id': selected_track_id,
    }
    return render(request, 'parallax/admin/teams.html', context)


@login_required(login_url='team_login')
def admin_marks(request):
    if not request.user.is_staff:
        return redirect('home')

    reviews = Review.objects.annotate(team_total=Count('marks')).order_by('scheduled_at')
    marks = Marks.objects.select_related('team', 'review', 'graded_by').order_by('-updated_at')
    if request.method == 'POST':
        action = request.POST.get('action', '').strip()

        if action == 'create_round':
            name = request.POST.get('name', '').strip()
            if not name:
                messages.error(request, 'Round name is required.')
            else:
                Review.objects.create(
                    name=name,
                    weightage=_parse_positive_int(request.POST.get('weightage')),
                    max_marks=_parse_positive_int(request.POST.get('max_marks')) or 100,
                )
                messages.success(request, f'Round "{name}" created.')
            return redirect('admin_marks')

        if action == 'delete_round':
            review = get_object_or_404(Review, id=request.POST.get('review_id'))
            name = review.name
            review.delete()
            messages.success(request, f'Round "{name}" deleted.')
            return redirect('admin_marks')

        if action == 'award_marks':
            review = get_object_or_404(Review, id=request.POST.get('review_id'))
            team = get_object_or_404(Team, id=request.POST.get('team_id'))
            raw_score = request.POST.get('score', '').strip()
            if not raw_score:
                messages.error(request, 'Enter a score to award marks.')
                return redirect('admin_marks')
            try:
                score = Decimal(raw_score)
            except (InvalidOperation, ValueError):
                messages.error(request, 'Enter a valid numeric score.')
                return redirect('admin_marks')

            Marks.objects.update_or_create(
                team=team,
                review=review,
                defaults={
                    'score': score,
                    'remarks': request.POST.get('remarks', '').strip(),
                    'graded_by': request.user,
                },
            )
            messages.success(request, f'Marks saved for {team.team_name} - {review.name}.')
            return redirect('admin_marks')

    reviews = Review.objects.annotate(team_total=Count('marks')).order_by('scheduled_at', 'name')
    teams = Team.objects.select_related('track').order_by('team_name')
    marks = Marks.objects.select_related('team', 'review', 'graded_by').order_by('-updated_at')
    total_weightage = sum(review.weightage for review in reviews)
    context = {
        'reviews': reviews,
        'teams': teams,
        'marks': marks,
        'total_weightage': total_weightage,
    }
    return render(request, 'parallax/admin/marks.html', context)


@login_required(login_url='team_login')
def admin_announcements(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()
        is_pinned = request.POST.get('is_pinned') == 'on'
        send_email = request.POST.get('send_email') == 'on'

        if not title or not body:
            messages.error(request, 'Announcement title and body are required.')
        else:
            Announcement.objects.create(
                title=title,
                body=body,
                is_pinned=is_pinned,
                send_email=send_email,
                created_by=request.user,
            )
            messages.success(request, 'Announcement created successfully.')
            return redirect('admin_announcements')

    announcements = Announcement.objects.all().order_by('-created_at')
    context = {'announcements': announcements}
    return render(request, 'parallax/admin/announcements.html', context)


@login_required(login_url='team_login')
def admin_tracks(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        action = request.POST.get('action', 'toggle_track')

        if action == 'add_problem_statement':
            track = get_object_or_404(Track, id=request.POST.get('track_id'))
            title = request.POST.get('title', '').strip()
            if not title:
                messages.error(request, 'Problem statement title is required.')
            else:
                ProblemStatement.objects.create(
                    track=track,
                    code=request.POST.get('code', '').strip(),
                    title=title,
                    description=_limit_text(request.POST.get('description')),
                    context=_limit_text(request.POST.get('context')),
                    impact=_limit_text(request.POST.get('impact')),
                    min_requirements=_limit_text(request.POST.get('min_requirements')),
                    dependencies=_limit_text(request.POST.get('dependencies')),
                    slot_capacity=_parse_positive_int(request.POST.get('slot_capacity')),
                    is_published=request.POST.get('is_published') == 'on',
                )
                messages.success(request, f'Problem statement "{title}" added.')
            return redirect(_admin_tracks_redirect(request))

        if action == 'edit_problem_statement':
            problem_statement = get_object_or_404(
                ProblemStatement, id=request.POST.get('problem_statement_id')
            )
            title = request.POST.get('title', '').strip()
            if not title:
                messages.error(request, 'Problem statement title is required.')
                return redirect(_admin_tracks_redirect(request))
            problem_statement.code = request.POST.get('code', '').strip()
            problem_statement.title = title
            problem_statement.description = _limit_text(request.POST.get('description'))
            problem_statement.context = _limit_text(request.POST.get('context'))
            problem_statement.impact = _limit_text(request.POST.get('impact'))
            problem_statement.min_requirements = _limit_text(request.POST.get('min_requirements'))
            problem_statement.dependencies = _limit_text(request.POST.get('dependencies'))
            problem_statement.slot_capacity = _parse_positive_int(request.POST.get('slot_capacity'))
            problem_statement.is_active = request.POST.get('is_active') == 'on'
            problem_statement.is_published = request.POST.get('is_published') == 'on'
            problem_statement.save()
            messages.success(request, f'Problem statement "{title}" saved.')
            return redirect(_admin_tracks_redirect(request))

        if action == 'update_slot_capacity':
            problem_statement = get_object_or_404(
                ProblemStatement, id=request.POST.get('problem_statement_id')
            )
            problem_statement.slot_capacity = _parse_positive_int(request.POST.get('slot_capacity'))
            problem_statement.is_active = request.POST.get('is_active') == 'on'
            problem_statement.save(update_fields=['slot_capacity', 'is_active', 'updated_at'])
            messages.success(request, f'Slots updated for "{problem_statement.title}".')
            return redirect(_admin_tracks_redirect(request))

        if action == 'toggle_problem_published':
            problem_statement = get_object_or_404(
                ProblemStatement, id=request.POST.get('problem_statement_id')
            )
            problem_statement.is_published = not problem_statement.is_published
            problem_statement.save(update_fields=['is_published', 'updated_at'])
            state_label = 'published' if problem_statement.is_published else 'unpublished'
            messages.success(request, f'"{problem_statement.title}" {state_label}.')
            return redirect(_admin_tracks_redirect(request))

        if action == 'delete_problem_statement':
            problem_statement = get_object_or_404(
                ProblemStatement, id=request.POST.get('problem_statement_id')
            )
            title = problem_statement.title
            problem_statement.delete()
            messages.success(request, f'Problem statement "{title}" deleted.')
            return redirect(_admin_tracks_redirect(request))

        track = get_object_or_404(Track, id=request.POST.get('track_id'))
        field = request.POST.get('field')
        if field in {'is_published', 'is_problem_live'}:
            setattr(track, field, not getattr(track, field))
            track.save(update_fields=[field, 'updated_at'])

        return redirect(_admin_tracks_redirect(request))

    selected_track_id = request.GET.get('track', '').strip()
    search_query = request.GET.get('q', '').strip()

    problem_statements = (
        ProblemStatement.objects.select_related('track')
        .annotate(booked_total=Count('booked_teams'))
        .order_by('track__name', 'code', 'title')
    )
    if selected_track_id:
        problem_statements = problem_statements.filter(track_id=selected_track_id)
    if search_query:
        problem_statements = problem_statements.filter(
            Q(title__icontains=search_query)
            | Q(code__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    context = {
        'tracks': Track.objects.annotate(team_total=Count('teams')).order_by('name'),
        'problem_statements': problem_statements,
        'selected_track_id': selected_track_id,
        'search_query': search_query,
    }
    return render(request, 'parallax/admin/tracks.html', context)


@login_required(login_url='team_login')
def admin_sponsors(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()

        if action == 'delete_sponsor':
            sponsor = get_object_or_404(Sponsor, id=request.POST.get('sponsor_id'))
            name = sponsor.name
            sponsor.delete()
            messages.success(request, f'Sponsor "{name}" deleted.')
            return redirect('admin_sponsors')

        name = request.POST.get('name', '').strip()
        sponsor_type = request.POST.get('sponsor_type', '').strip()
        if not name or sponsor_type not in dict(Sponsor.SPONSOR_TYPE_CHOICES):
            messages.error(request, 'Sponsor name and a valid sponsor type are required.')
            return redirect('admin_sponsors')

        if action == 'edit_sponsor':
            sponsor = get_object_or_404(Sponsor, id=request.POST.get('sponsor_id'))
        else:
            sponsor = Sponsor()

        sponsor.name = name
        sponsor.sponsor_type = sponsor_type
        sponsor.tagline = request.POST.get('tagline', '').strip()
        sponsor.display_order = _parse_positive_int(request.POST.get('display_order'))
        sponsor.is_active = request.POST.get('is_active') == 'on'
        if request.FILES.get('logo'):
            sponsor.logo = request.FILES['logo']
        sponsor.save()
        messages.success(request, f'Sponsor "{name}" saved.')
        return redirect('admin_sponsors')

    context = {
        'sponsors': Sponsor.objects.all(),
        'sponsor_type_choices': Sponsor.SPONSOR_TYPE_CHOICES,
    }
    return render(request, 'parallax/admin/sponsors.html', context)


def _admin_tracks_redirect(request):
    params = {}
    selected_track_id = request.POST.get('return_track') or request.GET.get('track')
    search_query = request.POST.get('return_q') or request.GET.get('q')
    if selected_track_id:
        params['track'] = selected_track_id
    if search_query:
        params['q'] = search_query
    url = reverse('admin_tracks')
    if params:
        return f'{url}?{urlencode(params)}'
    return url


def _limit_text(raw_value, limit=500):
    return (raw_value or '').strip()[:limit]


def _parse_positive_int(raw_value):
    try:
        return max(int(raw_value), 0)
    except (TypeError, ValueError):
        return 0

def build_home_stats(reviews):
    total_teams = Team.objects.count()
    total_participants = Participant.objects.filter(team__isnull=False).count()
    published_tracks = Track.objects.filter(is_published=True).count()

    return [
        {'number': total_teams or 0, 'label': 'Registered Teams'},
        {'number': total_participants or 0, 'label': 'Participants'},
        {'number': published_tracks or 0, 'label': 'Live Tracks'},
        {'number': reviews.count() or 0, 'label': 'Review Milestones'},
    ]


def build_default_track_cards():
    cards = []

    for index, track in enumerate(DEFAULT_TRACKS, start=1):
        cards.append(
            {
                'index': index,
                'name': track['name'],
                'icon': track['icon'],
                'description': track['description'],
                'prize': 'To be announced',
                'tag': 'Open for teams',
            }
        )

    return cards


def build_home_track_cards(published_tracks):
    cards = []

    for index, track in enumerate(published_tracks, start=1):
        normalized_name = track.name.strip().lower()
        prize = track.prize if hasattr(track, 'prize') else None
        cards.append(
            {
                'index': index,
                'name': track.name,
                'icon': TRACK_ICON_MAP.get(normalized_name, 'fa-bolt'),
                'description': track.description,
                'prize': prize.first_place if prize else 'To be announced',
                'tag': f'{track.team_total} teams',
            }
        )

    return cards


def get_released_problem_statement_sets(track, configuration):
    if not track or not track.is_problem_live:
        return []

    released_sets = []

    if configuration.set_one_released:
        released_sets.append(
            {
                'label': 'Problem Statement Set 1',
                'released_at': configuration.set_one_released_at,
                'items': parse_problem_statement_text(track.problem_statements_set_one or track.problem_statements),
            }
        )

    if configuration.set_two_released:
        released_sets.append(
            {
                'label': 'Problem Statement Set 2',
                'released_at': configuration.set_two_released_at,
                'items': parse_problem_statement_text(track.problem_statements_set_two),
            }
        )

    return released_sets


def parse_problem_statement_text(raw_text):
    cleaned_items = [line.strip('- ').strip() for line in raw_text.splitlines() if line.strip()]
    if cleaned_items:
        return cleaned_items
    return ['Problem statements for this set have not been added yet.']


def build_participant_progress(team, participant, problem_statement_sets, review_score_count):
    progress_items = [
        {
            'state': 'Complete',
            'tone': 'success',
            'description': 'Your participant profile is complete and linked to the team space.',
        },
        {
            'label': 'Team Access',
            'state': team.team_code,
            'tone': 'info',
            'description': f'You are currently part of {team.team_name}.',
        },
        {
            'label': 'Track Selection',
            'state': team.track.name if team.track else 'Pending',
            'tone': 'success' if team.track else 'pending',
            'description': 'The team leader can update the selected track until payment is confirmed.',
        },
        {
            'label': 'Review Status',
            'state': team.get_status_display(),
            'tone': 'success' if team.status == 'APPROVED' else 'danger' if team.status == 'REJECTED' else 'pending',
            'description': 'This is the current organizer review status of your team registration.',
        },
        {
            'label': 'Payment Reference',
            'state': 'Submitted' if team.invoice_number else 'Pending',
            'tone': 'success' if team.invoice_number else 'pending',
            'description': 'Participants only see whether the reference is submitted. Full payment details stay with OC.',
        },
        {
            'label': 'Payment Confirmation',
            'state': 'Confirmed' if team.payment_confirmed else 'Pending OC Check',
            'tone': 'success' if team.payment_confirmed else 'pending',
            'description': 'OC members confirm event hub payments from the organizer dashboard.',
        },
        {
            'label': 'Problem Statements',
            'state': f'{len(problem_statement_sets)} Set(s) Live' if problem_statement_sets else 'Awaiting Release',
            'tone': 'success' if problem_statement_sets else 'pending',
            'description': 'Released statements for your selected track appear here automatically.',
        },
        {
            'label': 'Evaluation',
            'state': f'{review_score_count} Review(s) Scored' if review_score_count else 'No Scores Yet',
            'tone': 'info' if review_score_count else 'pending',
            'description': 'Review marks are shown here only for your own team progress tracking.',
        },
    ]

    if participant.is_team_leader:
        progress_items.append(
            {
                'label': 'Leader Controls',
                'state': 'Enabled',
                'tone': 'info',
                'description': 'You can update the team name, track, and payment reference for your own team only.',
            }
        )

    return progress_items
def access_denied(request):
    return render(request, "parallax/access_denied.html")
