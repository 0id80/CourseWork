from django.shortcuts import render
from Hanoi import HanoiTowers

from json import loads
from random import randint, seed

from HanoiTowersApp.models import Iteration

from django.template.defaulttags import register


@register.filter
def full_data(value):
    if value is None:
        return []
    else:
        return [(index, name, scheme[::-1]) for index, name, scheme in zip(range(len(value)), range(len(value), 0, -1), value)]


@register.filter
def get_color(value):
    seed(value)
    rgb = (randint(0, 255), randint(0, 255), randint(0, 255))
    seed()
    return rgb


def index(request):
    hanoi = HanoiTowers(id="70151631")
    data = dict()
    data["iteration"] = hanoi.prepare_data
    data["disk_in_motion"] = dict()
    iterations = Iteration.objects.all()
    if len(iterations) < 100:
        data["calculate"] = True
    else:
        data["calculate"] = False

    if request.method == "GET":
        return render(request, "index.html", context={"data": data})

    if request.method == "POST":
        action = request.POST.get("step")

        if action == "calculate":
            hanoi.calculate_tower()
            print(action)

        elif action == "start":
            need_iteration = iterations.get(percent=0)
            data["iteration"] = loads(need_iteration.scheme)
        elif action == "end":
            data["iteration"] = loads(iterations.get(percent=100).scheme)
        else:
            # CALCULATE
            need_iteration = iterations.get(percent=int(action))
            disk = loads(need_iteration.disk_in_motion)
            data["iteration"] = loads(need_iteration.scheme)
            data["disk_in_motion"] = dict([("disk", disk[0]), ("from", disk[1]), ("to", disk[2])])
            print(data["disk_in_motion"])

        return render(request, "index.html", context={"data": data})
