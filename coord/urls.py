from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact_view, name='contact'),
    path('subscribe/', views.subscribe, name='subscribe'),
    # path('subscribe/success/', views.subscribe, name='subscribe_success'),
    path('events/add/', views.event_add, name='event_add'),
    path('events/all/', views.events_all, name='all_events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/<int:pk>/delete/', views.delete_event, name='event_delete'),
    path('event/<int:pk>/edit/', views.edit_event, name='event_edit'),


    path('gallery/add/', views.gallery_add, name='gallery_add'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('gallery/edit/<int:pk>/', views.gallery_edit, name='gallery_edit'),
    path('gallery/delete/<int:pk>/', views.gallery_delete, name='gallery_delete'),


    path('universities/', views.universities_all, name='all_universities'),
    path('universities/add/', views.university_add, name='university_add'),
    path('universities/<int:pk>/edit/', views.university_edit, name='university_edit'),
    path('universities/<int:pk>/delete/', views.university_delete, name='university_delete'),

    path('team/add/', views.team_add, name='team_add'),
    path('team/', views.team_all, name='all_team'),
    path('team/edit/<int:pk>/', views.team_edit, name='team_edit'),
    path('team/delete/<int:pk>/', views.team_delete, name='team_delete'),

    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('subscribers/', views.subscribers, name='subscribers'),
    path('subscribers/<int:pk>/delete/', views.subscriber_delete, name='subscriber_delete'),
    path('send-email/', views.send_bulk_email, name='send_bulk_email'),
    path('email-templates/', views.email_template_list, name='email_template_list'),
    path('email-templates/add/', views.email_template_create, name='email_template_create'),
    path('email-templates/<int:template_id>/edit/', views.email_template_edit, name='email_template_edit'),
    path('email-templates/<int:template_id>/send/', views.send_specific_bulk_email, name='send_specific_bulk_email'),
    path('email-templates/<int:template_id>/delete/', views.delete_template, name='delete_template'),


    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/<int:pk>/reply/', views.reply_to_message, name='reply_to_message'),

]
