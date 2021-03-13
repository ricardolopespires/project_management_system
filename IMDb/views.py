from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView ,DeleteView







class IndesTemplateView(TemplateView):
    template_name = 'initial/index.html'



class LancamentosTemplateView(TemplateView):
    template_name = 'initial/lancamentos.html'


class CartazTemplatesViews(TemplateView):
    template_name = 'initial/cartaz.html'