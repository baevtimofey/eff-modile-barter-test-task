from django.urls import path

from . import views

app_name = "barter_app"

urlpatterns = [
    path("", views.AdListView.as_view(), name="ad_list"),
]
