from django.urls import path
from Bank.views import index

urlpatterns = [
    path('', index, name="index"),
    path('calculate', index, name="index"),
    path('clear', index, name="index"),
]
