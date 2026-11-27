import json
import logging
from urllib.error import URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_safe

from .forms import ContactForm

logger = logging.getLogger(__name__)


@require_safe
def index(request):
    return render(request, "index.html", {"form": ContactForm()})


@require_http_methods(["GET", "HEAD", "POST"])
def contact_view(request):
    form = ContactForm(request.POST if request.method == "POST" else None)
    if request.method != "POST":
        return render(request, "index.html", {"form": form, "show_contact": True})

    status = 400
    if form.is_valid():
        if all((settings.RESEND_API_KEY, settings.CONTACT_FROM_EMAIL, settings.CONTACT_TO_EMAIL)):
            data = form.cleaned_data
            payload = {
                "from": settings.CONTACT_FROM_EMAIL,
                "to": [settings.CONTACT_TO_EMAIL],
                "reply_to": data["email"],
                "subject": f"Portfolio contact: {data['subject']}",
                "text": f"From: {data['name']} ({data['email']})\n\n{data['message']}",
            }
            delivery = Request(
                "https://api.resend.com/emails",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                    "Content-Type": "application/json",
                },
            )
            try:
                with urlopen(delivery, timeout=5):
                    return redirect("success")
            except (URLError, TimeoutError) as exc:
                logger.warning("Contact delivery failed (%s)", type(exc).__name__)
        form.add_error(None, "Your message could not be sent right now. Please try again later.")
        status = 503

    return render(request, "index.html", {"form": form, "show_contact": True}, status=status)


@require_safe
def download_brochure(request):
    brochure = settings.BASE_DIR / "static" / "files" / "AlanShajuwebsite.pdf"
    return FileResponse(brochure.open("rb"), as_attachment=True, filename="AlanShajuwebsite.pdf")
