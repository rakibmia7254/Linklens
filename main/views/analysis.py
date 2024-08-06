from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import ShortenedLink, Clicks
from django.http import HttpResponse, JsonResponse
import qrcode
from io import BytesIO
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page

User = get_user_model()


@login_required(login_url="login")
@cache_page(60 * 60 * 24 * 2)
def generate_qr_code(request, alias):
    data = f"https://is.gd/{alias}"
    try:
        link = ShortenedLink.objects.get(custom_alias=alias)
    except ShortenedLink.DoesNotExist:
        return JsonResponse({"error": "Link does not exist"})

    if link.user_id != request.user.id:
        return JsonResponse({"error": "Unauthorize"})
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = buffer.getvalue()
    return HttpResponse(img_str, content_type="image/png")


@login_required(login_url="login")
@cache_page(50)
def analysis_page(request, custom_alias):
    link = ShortenedLink.objects.get(custom_alias=custom_alias)

    if link.user_id != request.user.id:
        messages.error(request, "Please login first")
        return redirect("login")

    # Get the number of clicks for this link
    all_clicks = Clicks.objects.filter(url_id=link)

    data = (
        Clicks.objects.filter(url_id=link)
        .annotate(date=TruncDate("clicked_at"))
        .values("date")
        .annotate(count=Count("id"))
        .values("date", "count")
    )
    chart_data = [
        {"date": item["date"].isoformat(), "count": item["count"]} for item in data
    ]

    # browser
    browsers_count = [
        [item["browser"], item["count"]]
        for item in list(all_clicks.values("browser").annotate(count=Count("browser")))
    ]

    devices_count = [
        [item["device"], item["count"]]
        for item in list(all_clicks.values("device").annotate(count=Count("device")))
    ]

    countrys_count = [
        [item["country"], item["count"]]
        for item in list(all_clicks.values("country").annotate(count=Count("country")))
    ]

    return render(
        request,
        "dashboard/analysis.html",
        {
            "link": link.custom_alias,
            "click_data": chart_data,
            "clicks": all_clicks.count(),
            "browsers": browsers_count,
            "devices": devices_count,
            "countrys": countrys_count,
        },
    )


@login_required(login_url="login")
@cache_page(50)
def full_annalysis(request):
    all_clicks = Clicks.objects.filter(owner_id=request.user.id)

    data = (
        all_clicks.annotate(date=TruncDate("clicked_at"))
        .values("date")
        .annotate(count=Count("id"))
        .values("date", "count")
    )
    chart_data = [
        {"date": item["date"].isoformat(), "count": item["count"]} for item in data
    ]

    browsers_count = [
        [item["browser"], item["count"]]
        for item in list(all_clicks.values("browser").annotate(count=Count("browser")))
    ]

    devices_count = [
        [item["device"], item["count"]]
        for item in list(all_clicks.values("device").annotate(count=Count("device")))
    ]

    countrys_count = [
        [item["country"], item["count"]]
        for item in list(all_clicks.values("country").annotate(count=Count("country")))
    ]

    return render(
        request,
        "dashboard/analysis.html",
        {
            "click_data": chart_data,
            "clicks": all_clicks.count(),
            "browsers": browsers_count,
            "devices": devices_count,
            "countrys": countrys_count,
            "all_data": True,
        },
    )
