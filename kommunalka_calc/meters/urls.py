from django.urls import path

from .views import calculate, history

app_name = "meters"

urlpatterns = [
    path("", calculate, name="calculate"),
    path("history/", history, name="history"),
]
