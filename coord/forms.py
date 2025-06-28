from django import forms
from django.core.validators import validate_email, URLValidator
from django.core.exceptions import ValidationError
from .models import (
    UpcomingEvent, Program, Service, 
    GalleryItem, TeamMember, SubscriptionUser,
    Message, JobApplication, GeneralApplication,
    University, SubscriptionEmailTemplate
)
from phonenumber_field.formfields import PhoneNumberField

# 1. Upcoming Events Form
class UpcomingEventForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select the event date"
    )

    class Meta:
        model = UpcomingEvent
        fields = ['name', 'description', 'due_date', 'thumbnail', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Event name must be at least 3 characters long")
        return name

# 2. Programs Offered Form
class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'description', 'branch', 'duration']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

# 3. Services Offered Form
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

# 4. Gallery Form
class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['image', 'caption', 'occasion_title']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Optional caption'}),
            'occasion_title': forms.TextInput(attrs={'placeholder': 'Optional occasion title'}),
        }

# 5. Team Form
class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'rank', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

# 6. Subscription Forms
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionUser
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if SubscriptionUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed")
        return email

class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['full_name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your message...'}),
        }

        
class MessageReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your reply...'}),
        }

# 7. Job Application Form
class JobApplicationForm(forms.ModelForm):
    phone = PhoneNumberField(region='US', widget=forms.TextInput(attrs={'placeholder': '+1 (123) 456-7890'}))
    
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us why you\'d be a great fit...'}),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if resume.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Resume file too large (max 5MB)")
            if not resume.name.lower().endswith(('.pdf', '.doc', '.docx')):
                raise forms.ValidationError("Only PDF or Word documents are accepted")
        return resume

# 8. General Application Form
class GeneralApplicationForm(forms.ModelForm):
    phone = PhoneNumberField(region='US', widget=forms.TextInput(attrs={'placeholder': '+1 (123) 456-7890'}))
    
    class Meta:
        model = GeneralApplication
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us about your study goals...'}),
        }

# 9. Universities Form
class UniversityForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Application deadline date"
    )

    class Meta:
        model = University
        fields = ['name', 'description', 'acceptance_rate', 'location', 'deadline', 'website']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'website': forms.URLInput(attrs={'placeholder': 'https://university.edu'}),
        }

    def clean_acceptance_rate(self):
        rate = self.cleaned_data.get('acceptance_rate')
        try:
            rate_value = float(rate.strip('%'))
            if not 0 <= rate_value <= 100:
                raise ValueError
            return f"{rate_value}%"
        except ValueError:
            raise forms.ValidationError("Enter a valid percentage (e.g. '25%' or '45.5')")

    def clean_website(self):
        website = self.cleaned_data.get('website')
        validator = URLValidator()
        try:
            validator(website)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid website URL")
        return website
    
class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = SubscriptionEmailTemplate
        fields = ['subject', 'content', 'attachment']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Email content...'}),
        }
