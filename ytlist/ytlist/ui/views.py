from django.views.generic.base import TemplateView

from ytlist.logic.models import Video

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context

