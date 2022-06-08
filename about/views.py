# доп задание на зачет страница ABOUT

from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from business_notes.local_settings import SERVER_VERSION


class AboutView(View):
    def get(self, request):
        context = {
            "server_version": SERVER_VERSION,
            # "user": request.user,
        }
        return render(request, "about/about.html", context=context)


class AboutTemplateView(TemplateView):
    template_name = "about/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["server_version"] = SERVER_VERSION

        return context
