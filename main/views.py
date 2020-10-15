from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

from main.models import Product, Plan


class HomeView(TemplateView, LoginRequiredMixin):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.active().all()
        return context


class PlanListView(ListView, LoginRequiredMixin):
    model = Plan
    paginate_by = 3
    template_name = 'plan_list.html'

    def get_queryset(self):
        return Product.objects.active().get(pk=self.kwargs['product_id']).plans.active()
