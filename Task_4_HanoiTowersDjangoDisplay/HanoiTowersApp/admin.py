from django.contrib import admin
from HanoiTowersApp.models import Iteration


@admin.register(Iteration)
class IterationAdmin(admin.ModelAdmin):
    list_display = ("percent", "iteration_number", "scheme", "disk_in_motion")
