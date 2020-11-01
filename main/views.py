import datetime as ddt

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView

from main.forms import SubscriptionForm
from main.models import Product, Plan, Basket, BasketItem, Subscription


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.active().all()
        context['subscriptions'] = self.request.user.subscriptions.all()[:5]
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


@login_required
def delete_basket_item(request, basket_item_id):
    basket = request.basket
    if not basket:
        raise Http404('No basket provided')
    basket_item = get_object_or_404(BasketItem, pk=basket_item_id)
    basket_item.delete()
    return HttpResponseRedirect(reverse('main:home'))


class SubscriptionNewView(LoginRequiredMixin, TemplateView):
    template_name = 'subscription_new.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        plan_id = self.request.GET.get('plan_id')
        plan = get_object_or_404(Plan, pk=plan_id)
        ctx['plan'] = plan
        return ctx


@login_required
def create_subscription(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    plan_terms = {plan.period_unit: plan.period}
    this_time = ddt.datetime.now()
    # noinspection PyTypeChecker
    term_end = this_time + relativedelta(**plan_terms)
    subscription_data = dict(plan=plan, user=request.user, term_start=this_time,
                             term_end=term_end, status='New')
    subscription_form = SubscriptionForm(subscription_data)
    if subscription_form.is_valid():
        subscription_form.save()
        return HttpResponseRedirect(reverse('main:home'))


class SubscriptionListView(LoginRequiredMixin, ListView):
    template_name = 'subscriptions.html'
    model = Subscription

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class SubscriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Subscription
    template_name = 'subscription_update.html'
    fields = ['recurring', 'plan']
    success_url = reverse_lazy('main:subscriptions')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['plans'] = self.object.plan.product.plans.all()
        return ctx
