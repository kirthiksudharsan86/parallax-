from django.contrib import admin
from .models import (
    Announcement,
    EventConfiguration,
    Marks,
    Participant,
    Prize,
    ProblemStatement,
    Review,
    Sponsor,
    Team,
    Track,
)
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published','updated_at',)
    search_fields = ('name',)
    list_filter = ('is_published',)
@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ('track', 'first_place', 'second_place', 'third_place', 'updated_at',)
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_code', 'track',)
    search_fields = ('team_name', 'team_code',)
    list_filter = ('track',)
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'scheduled_at', 'max_marks', 'weightage')
@admin.register(EventConfiguration)
class EventConfigurationAdmin(admin.ModelAdmin):
    pass
@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "review",
        "score",
        "graded_by",
        "updated_at",
    )
    list_filter = ("review",)
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_pinned', 'send_email', 'created_by', 'created_at')
    list_filter = ('is_pinned', 'send_email')
    search_fields = ('title', 'body')
@admin.register(ProblemStatement)
class ProblemStatementAdmin(admin.ModelAdmin):
    list_display = ('title', 'track', 'code', 'slot_capacity', 'slots_filled', 'is_active', 'is_published')
    list_filter = ('track', 'is_active', 'is_published')
    search_fields = ('title', 'code', 'description')
@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'sponsor_type', 'is_active', 'display_order', 'updated_at')
    list_filter = ('sponsor_type', 'is_active')
    search_fields = ('name', 'tagline')