from django.contrib import admin
from .models import UpcomingEvent, University, Program, Service, GalleryItem, TeamMember, SubscriptionUser, SubscriptionEmailTemplate, JobApplication, GeneralApplication , Message
# Register your models here.
admin.site.register(UpcomingEvent)
admin.site.register(University)
admin.site.register(Service)
admin.site.register(GalleryItem)
admin.site.register(TeamMember)
admin.site.register(SubscriptionUser)
admin.site.register(Message)
admin.site.register(SubscriptionEmailTemplate)
admin.site.register(Program)
admin.site.register(JobApplication)
admin.site.register(GeneralApplication)
