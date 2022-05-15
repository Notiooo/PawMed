from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """Application main page (welcome page)"""
    template_name = 'homepage/homepage.html'
