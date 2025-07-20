from django.contrib import admin
from .models import (
    UpcomingEvent, Program, Service, GalleryItem,
    TeamMember, SubscriptionUser, Message,
    SubscriptionEmailTemplate, JobApplication,
    GeneralApplication, University
)

@admin.register(UpcomingEvent)
class UpcomingEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'due_date', 'location')
    search_fields = ('name', 'location')
    list_filter = ('due_date',)
    ordering = ('-due_date',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'duration', 'created_at')
    search_fields = ('name', 'branch')
    list_filter = ('branch',)
    ordering = ('-created_at',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('occasion_title', 'user', 'created_at')
    search_fields = ('occasion_title', 'caption')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank')
    search_fields = ('name', 'rank')


@admin.register(SubscriptionUser)
class SubscriptionUserAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'joined_at', 'replied_at', 'replied_by')
    search_fields = ('full_name', 'email')
    list_filter = ('joined_at', 'replied_at')
    ordering = ('-joined_at',)


@admin.register(SubscriptionEmailTemplate)
class SubscriptionEmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at')
    search_fields = ('subject',)
    ordering = ('-created_at',)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'submitted', 'applied_on')
    search_fields = ('full_name', 'email')
    list_filter = ('submitted', 'applied_on')
    ordering = ('-applied_on',)


@admin.register(GeneralApplication)
class GeneralApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_on')
    search_fields = ('name', 'email')
    ordering = ('-submitted_on',)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'acceptance_rate', 'deadline')
    search_fields = ('name', 'location')
    list_filter = ('deadline',)
    ordering = ('deadline',)
