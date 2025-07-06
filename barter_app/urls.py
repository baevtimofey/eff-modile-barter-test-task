from django.urls import path

from . import views

app_name = "barter_app"

urlpatterns = [
    # Маршруты для объявлений
    path("", views.AdListView.as_view(), name="ad_list"),
    path("new/", views.AdCreateView.as_view(), name="ad_create"),
    path("<int:pk>/", views.AdDetailView.as_view(), name="ad_detail"),
    path("<int:pk>/edit/", views.AdUpdateView.as_view(), name="ad_edit"),
    path("<int:pk>/delete/", views.AdDeleteView.as_view(), name="ad_delete"),
    # Маршруты для предложений обмена
    path(
        "<int:ad_id>/propose/",
        views.ExchangeProposalCreateView.as_view(),
        name="create_proposal",
    ),
    path("proposals/", views.ProposalsListView.as_view(), name="proposals"),
]
