from django.shortcuts import render, get_object_or_404
from .models import Track, Stat, TeamMember, Value, Domain


def home(request):
    context = {
        'tracks': Track.objects.filter(is_active=True),
        'stats':  Stat.objects.all(),
    }
    return render(request, 'home.html', context)


def about(request):
    context = {
        'team':   TeamMember.objects.all(),
        'values': Value.objects.all(),
    }
    return render(request, 'about.html', context)


def tracks(request):
    """Landing page: shows domain boxes (3 in row 1, 2 in row 2)."""
    context = {
        'domains': Domain.objects.filter(is_active=True),
    }
    return render(request, 'tracks.html', context)


def domain_detail(request, slug):
    """Detail page for a single domain: shows its problem statements
    as a 5x1 accordion matrix (description, context, minimum requirements,
    dependencies, rubric)."""
    domain = get_object_or_404(Domain, slug=slug, is_active=True)
    context = {
        'domain': domain,
        'problem_statements': domain.problem_statements.all().prefetch_related('rubric_criteria'),
    }
    return render(request, 'domain_detail.html', context)
