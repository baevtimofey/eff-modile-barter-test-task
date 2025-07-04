import django.views.generic

from . import models


class AdListView(django.views.generic.ListView):
    model = models.Ad
    template_name = "barter_app/ad_list.html"
    context_object_name = "ads"
    paginate_by = 10
