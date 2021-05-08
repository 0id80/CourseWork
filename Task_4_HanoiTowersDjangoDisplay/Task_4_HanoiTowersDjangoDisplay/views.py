from django.shortcuts import render
from Hanoi import HanoiTowers
from django.conf import settings

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
    data = dict([("id", hanoi.id),
                 ("name", settings.OWNER),
                 ("iteration", hanoi.prepare_data),
                 ("disk_in_motion", dict()),
                 ("percent", 0),
                 ("iteration_number", 0)
                 ])

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

        elif action == "start":
            need_iteration = iterations.get(percent=0)
            data["iteration"] = loads(need_iteration.scheme)
        elif action == "end":
            need_iteration = iterations.get(percent=100)
            data["iteration"] = loads(need_iteration.scheme)
            data["percent"] = need_iteration.percent
            data["iteration_number"] = need_iteration.iteration_number
        else:
            need_iteration = iterations.get(percent=int(action))
            disk = loads(need_iteration.disk_in_motion)
            data["iteration"] = loads(need_iteration.scheme)
            data["percent"] = need_iteration.percent
            data["iteration_number"] = need_iteration.iteration_number
            names_tower = {index: name for index, name in zip(range(0, len(data["iteration"])), range(len(data["iteration"]), 0, -1))}
            data["disk_in_motion"] = dict([("disk", disk[0]),
                                           ("from", disk[1]),
                                           ("to", disk[2]),
                                           ("from_name", names_tower.get(disk[1])),
                                           ("to_name", names_tower.get(disk[2]))])

        return render(request, "index.html", context={"data": data})
