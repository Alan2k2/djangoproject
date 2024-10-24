from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.mail import send_mail

def index(request):
    return render(request, 'index.html')

def contact_view(request):
    if request.method == 'POST':
        # Get the form data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Step 1: Send email using Django's email system
        try:
            send_mail(
                subject=f"New Contact Form Submission: {subject}",
                message=f"Message from {name} ({email}):\n\n{message}",
                from_email='alanshaju26@gmail.com',  # Replace with your email
                recipient_list=['alanshaju26@gmail.com'],  # Replace with recipient's email
            )
        except Exception as e:
            return HttpResponse(f"Error sending email: {e}")

        # Redirect to a success page after successful submission
        return redirect('../')

    # If GET request, show the form page
    return render(request, 'index.html')
