from django.shortcuts import render
from datetime import datetime


def hello_template(request, name):
    return render(
        request,
        "witaj/hello.html",
        {"name": name}
    )


def time(request):
    now = datetime.now()

    return render(
        request,
        "witaj/time.html",
        {
            "date": now.strftime("%d.%m.%Y"),
            "time": now.strftime("%H:%M"),
        }
    )
