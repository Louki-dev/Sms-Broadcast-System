from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Creating CONTACTS
class Contact(models.Model):
    contact_first_name = models.CharField(max_length=255, null=True)
    contact_last_name = models.CharField(max_length=255, null=True)
    contact_mobile_number = models.CharField(max_length=10, null=True)
    contact_email = models.EmailField(max_length=255, null=True)
    contact_status = models.SmallIntegerField(default='0')
    contact_created_at = models.DateTimeField(auto_now_add=True)
    contact_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_created_by', default='1')
    contact_updated_at = models.DateTimeField(null=True, default='2021-01-01 00:00:00.000000', blank=True)
    contact_last_joined = models.DateTimeField(null=True, default='2021-01-01 00:00:00.000000', blank=True)


# Creating OPT-IN
class Opt_in(models.Model):
    opt_in_mobile_number = models.CharField(max_length=255)
    opt_in_token = models.TextField()
    opt_in_status = models.SmallIntegerField(default='1')
    opt_in_created_at = models.DateTimeField(auto_now_add=True)
    opt_in_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opt_in_created_by', default='')
    opt_in_updated_at = models.DateTimeField(null=True, default='', blank=True)
    opt_out_at = models.DateTimeField(null=True, default='', blank=True)


# Creating Message
class Message(models.Model):
    message_content = models.TextField()
    message_status = models.SmallIntegerField(default='1')
    message_is_sent = models.SmallIntegerField(default='0')
    message_created_at = models.DateTimeField(auto_now_add=True)
    message_created_by = models.CharField(max_length=20)


# junction table between contacts/users and message table
class Sent_message(models.Model):
    sent_message_message = models.CharField(max_length=255)
    sent_message_contact = models.CharField(max_length=255)
    sent_message_created_at = models.DateTimeField(auto_now_add=True)
    sent_message_created_by = models.CharField(max_length=20)


