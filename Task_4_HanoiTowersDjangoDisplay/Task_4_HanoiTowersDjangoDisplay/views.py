from django.shortcuts import render
from Hanoi import HanoiTowers, to_output


def index(request):
    if request.method == "GET":
        return render(request, "index.html")

    if request.method == "POST":
        return render(request, "index.html")
