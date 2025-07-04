from django.urls import path

from . import views

app_name = "barter_app"

urlpatterns = [
    path("", views.AdListView.as_view(), name="ad_list"),
    path("new/", views.AdCreateView.as_view(), name="ad_create"),
    path("<int:pk>/edit/", views.AdUpdateView.as_view(), name="ad_edit"),
    path("<int:pk>/delete/", views.AdDeleteView.as_view(), name="ad_delete"),
]
