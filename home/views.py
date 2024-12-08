from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.http import FileResponse, Http404
from django.conf import settings
import os
import requests
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from user_agents import parse

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from user_agents import parse
import requests
from datetime import datetime

def index(request):
    return render(request, 'index.html')

# def contact_view(request):
#     if request.method == 'POST':
#         # Get the form data from POST request
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')

#         # Step 1: Send email using Django's email system
#         try:
#             send_mail(
#                 subject=f"New Contact Form Submission: {subject}",
#                 message=f"Message from {name} ({email}):\n\n{message}",
#                 from_email='alanshaju26@gmail.com',  # Replace with your email
#                 recipient_list=['alanshaju26@gmail.com'],  # Replace with recipient's email
#             )
#         except Exception as e:
#             return HttpResponse(f"Error sending email: {e}")

#         # Redirect to a success page after successful submission
#         return redirect('../')

#     # If GET request, show the form page
#     return render(request, 'index.html')

# def contact_view(request):
    if request.method == 'POST':
        # Get the form data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Step 1: Get user's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # Step 2: Fetch geolocation and timezone using IP
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            geo_data = response.json()
            location = f"{geo_data.get('city')}, {geo_data.get('country')}"
            time_zone = geo_data.get('timezone')
        except Exception as e:
            location = "Unknown"
            time_zone = "Unknown"

        # Step 3: Get device information
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        device_info = f"Device: {user_agent.device.family}, OS: {user_agent.os.family} {user_agent.os.version_string}, Browser: {user_agent.browser.family} {user_agent.browser.version_string}"

        # Step 4: Send email with additional data
        try:
            send_mail(
                subject=f"New Contact Form Submission: {subject}",
                message=f"Message from {name} ({email}):\n\n{message}\n\n"
                        f"IP Address: {ip_address}\n"
                        f"Location: {location}\n"
                        f"Time Zone: {time_zone}\n"
                        f"Device Info: {device_info}\n"
                        f"Submitted At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                from_email='alanshaju26@gmail.com',  # Replace with your email
                recipient_list=['alanshaju26@gmail.com'],  # Replace with recipient's email
            )
        except Exception as e:
            return HttpResponse(f"Error sending email: {e}")

        # Redirect to a success page after successful submission
        return redirect('../')

    # If GET request, show the form page
    return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from user_agents import parse
import requests
from datetime import datetime

def contact_view(request):
    if request.method == 'POST':
        # Get the form data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Step 1: Get user's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # Step 2: Fetch geolocation and timezone using IP
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            geo_data = response.json()
            location = f"{geo_data.get('city')}, {geo_data.get('country')}"
            time_zone = geo_data.get('timezone')
        except Exception as e:
            location = "Unknown"
            time_zone = "Unknown"

        # Step 3: Get device information
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        device_info = f"Device: {user_agent.device.family}, OS: {user_agent.os.family} {user_agent.os.version_string}, Browser: {user_agent.browser.family} {user_agent.browser.version_string}"

        # Step 4: Send email to admin
        try:
            send_mail(
                subject=f"New Contact Form Submission: {subject}",
                message=f"Message from {name} ({email}):\n\n{message}\n\n"
                        f"IP Address: {ip_address}\n"
                        f"Location: {location}\n"
                        f"Time Zone: {time_zone}\n"
                        f"Device Info: {device_info}\n"
                        f"Submitted At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                from_email='alanshaju26@gmail.com',  # Replace with your email
                recipient_list=['alanshaju26@gmail.com'],  # Replace with recipient's email
            )
        except Exception as e:
            return HttpResponse(f"Error sending email: {e}")

        # Step 5: Send acknowledgment email to the sender
        try:
            send_mail(
                subject="Thank you for contacting us!",
                message=f"Hello {name},\n\n"
                        f"Thank you for reaching out to us. This is an automated response to let you know "
                        f"that we've received your message. Our team will get back to you shortly.\n\n"
                        f"Best regards,\nThe Team\n\n"
                        f"Note: This is a no-reply email. Please do not respond directly to this email.",
                from_email='no.repay.alanshaju@gmail.com', 
                recipient_list=[email],
                auth_user='no.repay.alanshaju@gmail.com',
                auth_password='ngjr msbo haha afqn',
            )
        except Exception as e:
            return HttpResponse(f"Error sending acknowledgment email: {e}")

        # Redirect to a success page after successful submission
        return redirect('../')

    # If GET request, show the form page
    return render(request, 'index.html')


def download_brochure(request):
    file_path = os.path.join(settings.BASE_DIR, 'static/files/brochure.pdf')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='brochure.pdf')
    else:
        raise Http404