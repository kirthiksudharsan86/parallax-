from django.db import models


class Stat(models.Model):
    """Ticker stats shown on home page."""
    number = models.CharField(max_length=20, help_text='e.g. 5,000+')
    label  = models.CharField(max_length=100, help_text='e.g. Registered Builders')
    order  = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.number} — {self.label}'


class Track(models.Model):
    """Hackathon challenge tracks."""
    index       = models.CharField(max_length=4,   help_text='e.g. 01')
    icon        = models.CharField(max_length=10,  help_text='Emoji icon')
    name        = models.CharField(max_length=100)
    description = models.TextField()
    prize       = models.CharField(max_length=20,  help_text='e.g. $25,000')
    tag         = models.CharField(max_length=50,  help_text='e.g. AI / ML')
    order       = models.PositiveSmallIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Value(models.Model):
    """Core values shown on About page."""
    letter      = models.CharField(max_length=1)
    title       = models.CharField(max_length=100)
    description = models.TextField()
    order       = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    """Team members shown on About page."""
    name         = models.CharField(max_length=100)
    role         = models.CharField(max_length=100)
    bio          = models.TextField()
    avatar_emoji = models.CharField(max_length=10, default='👤')
    order        = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Domain(models.Model):
    """A challenge domain shown on the Tracks page (e.g. Edge AI & IoT).
    Each domain has its own detail page listing its problem statements."""
    slug        = models.SlugField(max_length=120, unique=True, help_text='Used in the URL, e.g. edge-ai-iot')
    icon        = models.CharField(max_length=10,  help_text='Emoji icon, e.g. 🤖')
    name        = models.CharField(max_length=150)
    tagline     = models.CharField(max_length=200, blank=True, help_text='Short line shown on the domain box')
    budget      = models.CharField(max_length=50,  default='₹2000 / team', help_text='e.g. ₹2000 / team')
    order       = models.PositiveSmallIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ProblemStatement(models.Model):
    """A single problem statement (PS) belonging to a Domain."""
    domain                = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='problem_statements')
    number                = models.PositiveSmallIntegerField(help_text='e.g. 1 for PS 1')
    title                 = models.CharField(max_length=200)
    description           = models.TextField()
    context                = models.TextField()
    minimum_requirements  = models.TextField(help_text='One requirement per line - rendered as a bullet list')
    dependencies          = models.TextField(help_text='One dependency per line - rendered as a bullet list')
    order                 = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'number']

    def __str__(self):
        return f'{self.domain.name} - PS {self.number}: {self.title}'

    def requirements_list(self):
        return [line.strip() for line in self.minimum_requirements.splitlines() if line.strip()]

    def dependencies_list(self):
        return [line.strip() for line in self.dependencies.splitlines() if line.strip()]


class RubricCriterion(models.Model):
    """A single row of a problem statement's grading rubric."""
    problem_statement = models.ForeignKey(ProblemStatement, on_delete=models.CASCADE, related_name='rubric_criteria')
    criterion          = models.CharField(max_length=150)
    weight             = models.CharField(max_length=10, help_text='e.g. 30%')
    notes              = models.CharField(max_length=200, blank=True)
    order              = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.criterion} ({self.weight})'
