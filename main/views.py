from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from main.models import Product, Plan, Basket, BasketItem


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.active().all()
        return context


class PlanListView(LoginRequiredMixin, ListView):
    model = Plan
    paginate_by = 3
    template_name = 'plan_list.html'

    def get_queryset(self):
        return Product.objects.active().get(pk=self.kwargs['product_id']).plans.active()


@login_required
def add_to_basket(request):
    plan_id = request.GET.get('plan_id')
    plan = get_object_or_404(Plan, pk=plan_id)
    basket = request.basket
    if not basket:
        basket = Basket.objects.create(user=request.user)
        request.session['basket_id'] = basket.id
    basket_item, created = BasketItem.objects.get_or_create(basket=basket, plan=plan)
    if not created:
        basket_item.quantity += 1
        basket_item.save()
    return HttpResponseRedirect(reverse('main:home'))
