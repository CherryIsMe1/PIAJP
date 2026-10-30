from datetime import datetime
from django.shortcuts import render

def hello_template(request, name):
    return render(request, "Lab1/hello.html", {"name": name})

def time(request):
    now = datetime.now()
    return render(request, "Lab1/time.html", {
        "date": now.strftime("%d.%m.%Y"),
        "time": now.strftime("%H:%M"),
    })
