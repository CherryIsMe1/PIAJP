from datetime import datetime
from django.shortcuts import render


def time(request):
    now = datetime.now()

    return render(request, "time.html", {
        "date": now.strftime("%d.%m.%Y"),
        "time": now.strftime("%H:%M"),
    })
