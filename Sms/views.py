from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Contact, Message, Opt_in, Sent_message
from .forms import Contact_form, Message_form
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def how_to_opt_in(request):
    return render(request, 'opt_in.html')


def about_request(request):
    return render(request, 'about.html')


def adminView(request):
    contacts = Contact.objects.all().count()
    contacts_active = Contact.objects.filter(contact_status=1).count()
    contacts_inactive = Contact.objects.filter(contact_status=0).count()
    opt_in = Opt_in.objects.all().count()
    opt_active = Opt_in.objects.filter(opt_in_status=1).count()
    opt_inactive = Opt_in.objects.filter(opt_in_status=0).count()
    admins = User.objects.filter(is_staff=0).order_by('-id')
    context = {'contacts': contacts, 'contacts_active': contacts_active, 'contacts_inactive': contacts_inactive,
               'opt_in': opt_in, 'opt_active':opt_active, 'opt_inactive': opt_inactive, 'admins':admins}
    return render(request, 'dashboard.html', context)


def Contact_view(request):
    contacts = Contact.objects.all().order_by('-id')
    count_contacts = Contact.objects.filter(contact_status=1).count()
    return render(request, 'contacts.html', {'count_contacts': count_contacts, 'contacts':contacts})


def Opt_in_users(request):
    opt_ins = Opt_in.objects.all().order_by('-id')
    count_opt_ins= Opt_in.objects.filter(opt_in_status=1).count()
    return render(request, 'opt_in_users.html', {'opt_ins': opt_ins, 'count_opt_ins':count_opt_ins})


def Contact_add(request):
    if request.method == "POST":
        form = Contact_form(request.POST)
        if form.is_valid():
            form.save()
        else:
            contact_first_name = request.POST['contact_first_name']
            contact_last_name = request.POST['contact_last_name']
            contact_mobile_number = request.POST['contact_mobile_number']
            contact_email = request.POST['contact_email']
            context = {
                'contact_first_name': contact_first_name,
                'contact_last_name': contact_last_name,
                'contact_mobile_number': contact_mobile_number,
                'contact_email': contact_email
            }
            messages.error(request, 'There was an error in your form. Please try again.')
            return render(request, 'contact_form.html', context)
        messages.success(request, 'Please follow the instructions below to have an access to the system.')
        return redirect('/new/opt-in/')
    else:
        form = Contact_form()
    return render(request, 'contact_form.html', {'form': form})


class Create_message(CreateView):
    model = Message
    template_name = "create_message.html"
    form_class = Message_form
    success_url = reverse_lazy('junction')


@csrf_exempt  # this will not require csrf_token to handle post requests
def Globelabs_api(request):
    if request.method == 'GET':
        access_token = request.GET.get('access_token', None)
        subscriber_number = request.GET.get('subscriber_number', None)
        created_by = User.objects.get(id=1)
        opt = Opt_in.objects.filter(opt_in_mobile_number=subscriber_number)
        datetime = timezone.now()
        if not opt:  # if walay pay records, create
            opt_create = Opt_in.objects.create(opt_in_mobile_number=subscriber_number, opt_in_token=access_token, opt_in_updated_at="2021-01-01 00:00:00.000000", opt_out_at="2021-01-01 00:00:00.000000", opt_in_created_by=created_by,  opt_in_status=1)
            opt_create.save()
            contact_status = Contact.objects.filter(contact_mobile_number=subscriber_number).update(contact_status=1)
        else:  # if naa nay records, update
            opt_update = Opt_in.objects.filter(opt_in_mobile_number=subscriber_number).update(opt_in_mobile_number=subscriber_number, opt_in_token=access_token, opt_in_updated_at=datetime, opt_in_status=1)
            contact_update = Contact.objects.filter(contact_mobile_number=subscriber_number).update(contact_status=1, contact_updated_at=datetime)
        return HttpResponse(access_token, subscriber_number)

    else:
        received_json_data = json.loads(request.body)
        json_data = received_json_data['unsubscribed']
        subscriber_number = json_data['subscriber_number']
        datetime = json_data['timestamp']
        opt = Opt_in.objects.filter(opt_in_mobile_number=subscriber_number)
        if not opt:
            pass
        else:
            opt_update_status = Opt_in.objects.filter(opt_in_mobile_number=subscriber_number).update(opt_in_status=0, opt_in_mobile_number=subscriber_number, opt_out_at=datetime)
            contact_update_status = Contact.objects.filter(contact_mobile_number=subscriber_number).update(contact_status=0, contact_last_joined=datetime)
        return HttpResponse(subscriber_number)


def junction(request):
    if request.method == "GET":
        a = Message.objects.last()  # fetch the recent post message
        message = a.id
        b = Sent_message.objects.filter(sent_message_message=message)
        if not b:
            for c in Opt_in.objects.filter(opt_in_status=1):
                sent_table = Sent_message.objects.create(sent_message_message=message, sent_message_contact=c.opt_in_mobile_number, sent_message_created_by=a.message_created_by)
                sent_table.save()
            sql = Sent_message.objects.raw('SELECT * FROM sms_sent_message LEFT JOIN sms_opt_in ON sent_message_contact = sms_opt_in.opt_in_mobile_number LEFT JOIN sms_message ON sms_message.id = sent_message_message WHERE sms_opt_in.opt_in_status = 1 and sent_message_message =' + str(message))
            for d in sql:
                sent_execution(d)
            update_message_sent = Message.objects.filter(message_is_sent=0).update(message_is_sent=1)
        else:
            pass
    messages.success(request, 'Your message has been broadcasted successfully!')
    return redirect('/user/admin/dashboard/')


def sent_execution(fetch):
    access_token = fetch.opt_in_token
    message = fetch.message_content
    shortcode = '3911'
    clientCorrelator = '225653911' # uniquely identifies this create SMS request.
    address = fetch.sent_message_contact

    url = "https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/" + shortcode + "/requests"

    querystring = {"access_token": access_token}

    payload = "{\"outboundSMSMessageRequest\": { \"clientCorrelator\": \"" + clientCorrelator + "\", \"senderAddress\": \"" + shortcode + "\", \"outboundSMSTextMessage\": {\"message\": \"" + message + "\"}, \"address\": \"" + address + "\" } }"
    headers = {'Content-Type': "application/json", 'Host': "devapi.globelabs.com.ph"}

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        display_lname = Contact.objects.filter(contact_last_name__icontains=searched)
        display_num = Contact.objects.filter(contact_mobile_number__icontains=searched)
        return render(request, 'search.html', {'searched': searched, 'display_lname': display_lname, 'display_num':display_num})
    else:
        return render(request, 'search.html', {})

