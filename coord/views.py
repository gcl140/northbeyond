from django.utils.timezone import now
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactForm, SubscriptionForm, UpcomingEventForm, GalleryItemForm, UniversityForm, TeamMemberForm, EmailTemplateForm, MessageReplyForm, ProgramForm, JobApplicationForm
from .models import Message, SubscriptionUser, UpcomingEvent, GalleryItem, University, TeamMember, SubscriptionEmailTemplate, Program, JobApplication
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('landing')  # Adjust this redirect as needed
    else:
        form = ContactForm()
    return render(request, 'your_template_path/contact.html', {'form': form})


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscription, created = SubscriptionUser.objects.get_or_create(email=email)

            if created:
                # Only send confirmation if it's a new subscription
                subject = "✅ You're Subscribed to North & Beyond!"
                html_content = render_to_string("coord/subscription_confirmation.html", {
                    'email': email,
                    'current_year': date.today().year,
                })
                plain_text = strip_tags(html_content)
                email_msg = EmailMultiAlternatives(subject, plain_text, to=[email])
                email_msg.attach_alternative(html_content, "text/html")
                email_msg.send()

                messages.success(request, "Thank you for subscribing! A confirmation email has been sent.")
            else:
                messages.info(request, "You're already subscribed to our list.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    return redirect('landing')

def events_all(request):
    events = UpcomingEvent.objects.order_by('-due_date')
    return render(request, 'coord/events_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(UpcomingEvent, pk=pk)
    today = date.today()
    delta = (event.due_date - today).days

    if delta == 0:
        status = "Happening Today!"
    elif delta > 0:
        status = f"{delta} day{'s' if delta > 1 else ''} left"
    else:
        status = "Deadline Passed"

    context = {
        'event': event,
        'event_status': status,
    }
    return render(request, 'coord/event_detail.html', context)

@staff_member_required
def event_add(request):
    if request.method == 'POST':
        form = UpcomingEventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_events')
    else:
        form = UpcomingEventForm()
    return render(request, 'coord/event_add.html', {'form': form, 'title': 'Create New'})


@staff_member_required
def edit_event(request, pk):
    event = get_object_or_404(UpcomingEvent, pk=pk)
    if request.method == 'POST':
        form = UpcomingEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('event_detail', pk=event.pk)
    else:
        form = UpcomingEventForm(instance=event)
    return render(request, 'coord/event_add.html', {'form': form, 'event': event, 'title': 'Edit'})


@staff_member_required
def delete_event(request, pk):
    event = get_object_or_404(UpcomingEvent, pk=pk)
    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('all_events')  # or 'landing' depending on your structure


@staff_member_required
def gallery_add(request):
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Gallery item added.")
            return redirect('gallery')
    else:
        form = GalleryItemForm()
    return render(request, 'coord/gallery_add.html', {'form': form, 'title': 'Add'})

@staff_member_required
def gallery_edit(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Gallery item updated.")
            return redirect('gallery')
    else:
        form = GalleryItemForm(instance=item)
    return render(request, 'coord/gallery_add.html', {'form': form, 'title': 'Edit', 'item': item})

@staff_member_required
def gallery_delete(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    item.delete()
    messages.success(request, "Gallery item deleted.")
    return redirect('gallery')


def gallery_view(request):
    gallery_items = GalleryItem.objects.order_by('-created_at')
    return render(request, 'coord/gallery.html', {'gallery_items': gallery_items})


def universities_all(request):
    universities = University.objects.order_by('deadline')
    return render(request, 'coord/universities.html', {'universities': universities})

@staff_member_required
def university_add(request):
    if request.method == 'POST':
        form = UniversityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "University added successfully.")
            return redirect('all_universities')
    else:
        form = UniversityForm()
    return render(request, 'coord/university_add.html', {'form': form, 'title': 'Add'})

@staff_member_required
def university_edit(request, pk):
    university = get_object_or_404(University, pk=pk)
    if request.method == 'POST':
        form = UniversityForm(request.POST, instance=university)
        if form.is_valid():
            form.save()
            messages.success(request, "University updated successfully.")
            return redirect('all_universities')
    else:
        form = UniversityForm(instance=university)
    return render(request, 'coord/university_add.html', {'form': form, 'title': 'Edit', 'university': university})

@staff_member_required
def university_delete(request, pk):
    university = get_object_or_404(University, pk=pk)
    university.delete()
    messages.success(request, "University deleted.")
    return redirect('all_universities')

def team_all(request):
    team_members = TeamMember.objects.all().order_by('rank')
    return render(request, 'coord/team.html', {'team_members': team_members})

@staff_member_required
def team_add(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Team member added successfully.")
            return redirect('all_team')
    else:
        form = TeamMemberForm()
    return render(request, 'coord/team_add.html', {'form': form, 'title': 'Add'})

@staff_member_required
def team_edit(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Team member updated successfully.")
            return redirect('all_team')
    else:
        form = TeamMemberForm(instance=member)
    return render(request, 'coord/team_add.html', {'form': form, 'title': 'Edit', 'member': member})

@staff_member_required
def team_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    member.delete()
    messages.success(request, "Team member removed.")
    return redirect('all_team')

@staff_member_required
def staff_dashboard(request):
    return render(request, 'coord/actions.html', {'title': 'Staff Dashboard'})

@staff_member_required
def subscribers(request):
    query = request.GET.get('q', '')
    users = SubscriptionUser.objects.all().order_by('email')
 
    if query:
        users = users.filter(
            Q(email__icontains=query)
        )
    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'coord/email_all_subscribers.html', context)

@staff_member_required
def subscriber_delete(request, pk):
    user = get_object_or_404(SubscriptionUser, pk=pk)
    user.delete()
    messages.success(request, "Subscriber removed successfully.")
    return redirect('subscribers')



@staff_member_required
def send_bulk_email(request):
    if request.method == "POST":
        form = EmailTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            email_template = form.save()

            users = SubscriptionUser.objects.all()
            recipient_list = [user.email for user in users]

            html_content = email_template.content
            plain_content = strip_tags(html_content)
            subject = email_template.subject

            email = EmailMultiAlternatives(subject, plain_content, to=recipient_list)
            email.attach_alternative(html_content, "text/html")
            if email_template.attachment:
                email.attach(email_template.attachment.name, email_template.attachment.read())

            email.send()
            messages.success(request, "Email sent to all waitlist users!")
            return redirect("subscribers")
        else:
            messages.error(request, "Error sending email.")

    else:
        form = EmailTemplateForm()

    return render(request, "coord/email_subscribers.html", {"form": form})





# List email templates
@staff_member_required
def email_template_list(request):
    templates = SubscriptionEmailTemplate.objects.all()
    return render(request, 'coord/email_template_list.html', {'templates': templates})


# Edit an existing template
@staff_member_required
def email_template_edit(request, template_id):
    template = get_object_or_404(SubscriptionEmailTemplate, id=template_id)

    if request.method == "POST":
        form = EmailTemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, "Template edited successfully")
            return redirect('email_template_list')
    else:
        form = EmailTemplateForm(instance=template)
    return render(request, 'coord/email_template_form.html', {'form': form})

@staff_member_required
def email_template_create(request):
    if request.method == "POST":
        form = EmailTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Template created successfully")
            return redirect('email_template_list')
    else:
        form = EmailTemplateForm()

    return render(request, 'coord/email_template_form.html', {'form': form})

@staff_member_required
def delete_template(request, template_id):
    template = get_object_or_404(SubscriptionEmailTemplate, id=template_id)
    template.delete()
    messages.success(request, "Email template deleted successfully.")
    return redirect("email_template_list")

@staff_member_required
def send_specific_bulk_email(request, template_id):
    template = get_object_or_404(SubscriptionEmailTemplate, id=template_id)
    users = SubscriptionUser.objects.values_list("email", flat=True)

    if not users:
        messages.warning(request, "No users found in the subscription list.")
        return redirect('email_template_list')

    subject = template.subject
    content = template.content
    attachment = template.attachment
    html_message = render_to_string("coord/email_subscribers.html", {"subject": subject, "content": content, "attachment": attachment, "current_year": date.today().year})
    plain_message = strip_tags(html_message)

    try:
        email = EmailMultiAlternatives(subject, plain_message, to=list(users))
        email.attach_alternative(html_message, "text/html")
        if attachment:
            email.attach_file(attachment.path)
        email.send()

        messages.success(request, f"Email successfully sent to {len(users)} users.")
    except Exception as e:
        messages.error(request, f"Error sending email: {e}")

    return redirect('email_template_list')


@staff_member_required
def message_list(request):
    messages_qs = Message.objects.all().order_by('-joined_at')  # adjust field if needed
    return render(request, 'coord/message_list.html', {'mesejes': messages_qs})

@staff_member_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return render(request, 'coord/message_detail.html', {'meseje': message})

@staff_member_required
def reply_to_message(request, pk):
    msg = get_object_or_404(Message, pk=pk)

    if request.method == 'POST':
        form = MessageReplyForm(request.POST, instance=msg)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.replied_at = now()
            reply.replied_by = request.user
            reply.save()

            # Send email reply
            subject = f"Reply from North & Beyond"
            html_content = render_to_string("coord/message_reply_email.html", {
                'message': msg,
                'reply': reply.reply,
                'current_year': date.today().year
            })
            plain_text = strip_tags(html_content)

            email = EmailMultiAlternatives(subject, plain_text, to=[msg.email])
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(request, "Reply sent and recorded.")
            return redirect('message_detail', pk=pk)
    else:
        form = MessageReplyForm(instance=msg)

    return render(request, 'coord/message_reply_form.html', {'form': form, 'message': msg})

@staff_member_required
def program_list(request):
    programs = Program.objects.all().order_by('name')
    return render(request, 'coord/programs_list.html', {'programs': programs})

@staff_member_required
def program_create(request):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Program created successfully.")
            return redirect('program_list')
    else:
        form = ProgramForm()
    return render(request, 'coord/programs_add.html', {'form': form, 'title': 'Add Program'})

@staff_member_required
def program_edit(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == "POST":
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, "Program updated successfully.")
            return redirect('program_list')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'coord/programs_add.html', {'form': form, 'title': 'Edit Program'})

@staff_member_required
def program_delete(request, pk):
    program = get_object_or_404(Program, pk=pk)
    program.delete()
    messages.success(request, "Program deleted successfully.")
    return redirect('program_list')

@staff_member_required
def program_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    return render(request, 'coord/program_detail.html', {'program': program})


@login_required
def apply_for_job(request):
    # Check if the user has already submitted
    if JobApplication.objects.filter(user=request.user, submitted=True).exists():
        messages.info(request, "You have already submitted an application.")
        return redirect("job_apply_success")

    # Check if there's a saved draft (submitted=False)
    existing_app = JobApplication.objects.filter(user=request.user, submitted=False).first()

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES, instance=existing_app)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.submitted = True  # mark as submitted
            application.save()
            messages.success(request, "Your application has been submitted successfully.")
            return redirect("job_apply_success")
    else:
        form = JobApplicationForm(instance=existing_app)

    return render(request, "coord/job_application_form.html", {
        "form": form,
        "title": "Apply as Intern"
    })

def job_apply_success(request):
    return render(request, "coord/job_success.html")

@staff_member_required
def my_applications(request):
    apps = JobApplication.objects.filter(user=request.user, submitted=True).order_by('-applied_on')
    return render(request, "coord/job_apps.html", {"applications": apps})

@staff_member_required
def delete_application(request, pk):
    app = get_object_or_404(JobApplication, pk=pk, user=request.user)
    app.delete()
    messages.success(request, "Application deleted successfully.")
    return redirect("my_applications")