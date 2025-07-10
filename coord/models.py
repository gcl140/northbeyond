from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

# 1. Upcoming Events
class UpcomingEvent(models.Model):
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='events/thumbnails/', blank=True, null=True)
    description = models.TextField()
    due_date = models.DateField()
    location = models.CharField(max_length=255, default='Golden Tulip, DSM')

# 2. Programs Offered
class Program(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    branch = models.CharField(max_length=255, choices=[
        ('All Branches', 'All Branches'),
        ('Golden Tulip, DSM', 'Golden Tulip, DSM'),
        ('Seychelles', 'Seychelles'),
        ('Arusha, DSM', 'Arusha, DSM')
    ], default='All Branches' )
    duration = models.CharField(max_length=100, null= True, blank=True )
    # type = models.CharField(max_length=50, choices=[
    #     ('Short Course', 'Short Course'),
    #     ('Diploma', 'Diploma'),
    #     ('Certificate', 'Certificate'),
    #     ('Degree', 'Degree'),
    #     ('Masters', 'Masters'),
    #     ('PhD', 'PhD')
    # ], default='Short Course')
    created_at = models.DateTimeField(auto_now_add=True)

# 3. Services Offered
class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

# 4. Gallery
class GalleryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='gallery/')
    occasion_title = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# 5. Team
class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='team/')

# 6. Subscription Section
class SubscriptionUser(models.Model):
    email = models.EmailField(unique=True)  # Ensure unique emails
    
class Message(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  # Ensure unique emails
    joined_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)  # Optional message field

        # New reply fields
    reply = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    replied_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name}"

class SubscriptionEmailTemplate(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    attachment = models.FileField(upload_to="email_attachments/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
# 7. Apply for a Job
class JobApplication(models.Model):
    full_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    submitted = models.BooleanField(default=False)  # Add this
    applied_on = models.DateTimeField(auto_now_add=True)

# 8. Apply With Us
class GeneralApplication(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)

# 9. Universities
class University(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    acceptance_rate = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    deadline = models.DateField()
    website = models.URLField()
