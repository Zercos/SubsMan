import datetime as ddt

from dateutil.relativedelta import relativedelta
from django.test.testcases import TestCase
from django.urls import reverse

from main.tests.factories import PlanFactory, ProductFactory
from user.tests.factories import UserFactory


class TestViews(TestCase):
    def test_home_page(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)

    def test_plan_list_view(self):
        product = ProductFactory()
        PlanFactory.create_batch(4, product=product)
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('main:plans', kwargs={'product_id': product.id}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.context['page_obj']))
        self.assertEqual(product.plans.active().all()[0], response.context['plan_list'][0])

    def test_add_to_basket(self):
        user = UserFactory()
        product = ProductFactory()
        plan = PlanFactory(product=product)

        self.client.force_login(user)
        self.client.get(reverse('main:add_to_basket'), {'plan_id': plan.id})
        self.assertTrue(user.basket_set.filter(user=user).exists())
        self.assertTrue(user.basket_set.filter(user=user).first().basketitem_set.filter(plan=plan).exists())

    def test_create_subscription(self):
        user = UserFactory()
        product = ProductFactory()
        plan = PlanFactory(product=product, period=4, period_unit='months')
        term_end = ddt.datetime.now() + relativedelta(months=4)

        self.client.force_login(user)
        response = self.client.get(reverse('main:create_subscription', kwargs={'plan_id': plan.id}))
        self.assertEqual(302, response.status_code)
        self.assertTrue(plan.subscriptions.exists())
        self.assertEqual(plan.subscriptions.first().term_start.date(), ddt.date.today())
        self.assertEqual(plan.subscriptions.first().term_end.date(), term_end.date())
