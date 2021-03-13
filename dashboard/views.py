from django.shortcuts import render
from django.views.generic import View,ListView,TemplateView, DetailView
# Create your views here.





class DashboardTemplateView(TemplateView):
    template_name = 'dashboard/index.html'



