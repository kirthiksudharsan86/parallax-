from django.contrib import admin
from .models import Stat, Track, Value, TeamMember, Domain, ProblemStatement, RubricCriterion


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('number', 'label', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display  = ('index', 'name', 'prize', 'tag', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter   = ('is_active',)
    ordering      = ('order',)


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display  = ('letter', 'title', 'order')
    list_editable = ('order',)
    ordering      = ('order',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display  = ('name', 'role', 'order')
    list_editable = ('order',)
    ordering      = ('order',)


class RubricCriterionInline(admin.TabularInline):
    model = RubricCriterion
    extra = 1


@admin.register(ProblemStatement)
class ProblemStatementAdmin(admin.ModelAdmin):
    list_display  = ('domain', 'number', 'title', 'order')
    list_filter   = ('domain',)
    ordering      = ('domain', 'order', 'number')
    inlines       = [RubricCriterionInline]


class ProblemStatementInline(admin.TabularInline):
    model = ProblemStatement
    extra = 0
    fields = ('number', 'title', 'order')
    show_change_link = True


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug', 'budget', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter   = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    ordering      = ('order',)
    inlines       = [ProblemStatementInline]
