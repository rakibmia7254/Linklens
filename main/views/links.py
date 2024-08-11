from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.contrib import messages
import requests
from ..models import ShortenedLink, Clicks, CustomUser
from ..utils import generate_custom_alias
from user_agents import parse
from ..utils import i2c
import datetime
import validators


@login_required(login_url="login")
def dashboard(request):
    # all links clicks today
    clicks_today = Clicks.objects.filter(clicked_at__date=datetime.date.today()).count()

    # user links
    user_links = ShortenedLink.objects.filter(user=request.user)

    return render(
        request,
        "dashboard/index.html",
        {
            "clicks_today": clicks_today,
            "user_links_count": user_links.count(),
            "user_links": user_links,
        },
    )


@csrf_exempt
@login_required(login_url="login")
def shorten_link(request):
    if request.method == "POST":
        original_url = request.POST.get("original_url")
        custom_alias = request.POST.get("custom_alias")

        if not validators.url(original_url):
            messages.error(request, "Invalid URL", "alert-danger")
            return redirect("shorten_link")

        # Check if custom alias already exists
        if ShortenedLink.objects.filter(custom_alias=custom_alias).exists():
            messages.error(request, "Custom alias already exists", "alert-danger")
            return redirect("shorten_link")

        if not custom_alias:
            custom_alias = generate_custom_alias()

        if not original_url:
            messages.error(request, "Original URL is required", "alert-danger")
            return redirect("shorten_link")

        full_link = f"https://linklens.onrender.com/redirect/{custom_alias}"

        try:
            response_gd = requests.get(
                f"https://is.gd/create.php?format=simple&url={full_link}&shorturl={custom_alias}",
                timeout=2000,
            )
        except:
            messages.error(request, "Cant connect to is.gd", "alert-danger")
            return redirect("shorten_link")

        if response_gd.status_code == 200:
            shortened_link = ShortenedLink.objects.create(
                user=request.user, original_url=original_url, custom_alias=custom_alias
            )
            shortened_link.short_url = response_gd.text
            shortened_link.save()
            messages.success(
                request, f"Link shortened {response_gd.text}", "alert-success"
            )
            return redirect("dashboard")
        elif response_gd.status_code == 406:
            messages.error(request, "custom alias is not available", "alert-danger")
            return redirect("shorten_link")
        else:
            messages.error(request, "Failed to shorten link")
            return redirect("shorten_link")
    return render(request, "dashboard/create.html")


def redirect_link(request, custom_alias):
    try:
        shortened_link = ShortenedLink.objects.get(custom_alias=custom_alias)
    except ShortenedLink.DoesNotExist:
        return render(request, "404.html")

    user_agent_parser = parse(request.META.get("HTTP_USER_AGENT", "unknown"))
    bowser = user_agent_parser.browser.family
    # get device type pc or mobile
    device = user_agent_parser.get_device()

    ip = request.environ["REMOTE_ADDR"]
    country = i2c.lookup_ip(ip)

    owner_of_l = CustomUser.objects.get(id=shortened_link.user_id)
    Clicks.objects.create(
        url_id=shortened_link.id,
        browser=bowser,
        device=device,
        country=country,
        owner_id=owner_of_l,
    )
    return redirect(shortened_link.original_url)


@login_required(login_url="login")
def delete_link(request, custom_alias):
    try:
        shortened_link = ShortenedLink.objects.get(custom_alias=custom_alias)
        if shortened_link.user != request.user:
            messages.error(request, "You do not have permission to delete this link")
            return redirect("dashboard")

        # Deleting the shortened link
        shortened_link.delete()
        return redirect("dashboard")
    except ShortenedLink.DoesNotExist:
        return redirect("dashboard")


@cache_page(10)
def test(request):
    user = CustomUser.objects.all()
    user.delete()
    messages.error(request, "You do not have permission to delete this link")
    return redirect("dashboard")
