from datetime import datetime

from django.shortcuts import render


def index(request):
    return render(request, "hello/index.html")


def hello_template(request, name):
    return render(request, "hello/hello.html", {"name": name})


def time(request):
    now = datetime.now()
    return render(request, "hello/time.html", {
        "date": now.strftime("%d.%m.%Y"),
        "time": now.strftime("%H:%M"),
    })
