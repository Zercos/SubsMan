import datetime as ddt

from django.test.testcases import TestCase

from main.services import disactivate_expired_subscriptions
from main.tests.factories import SubscriptionFactory


class TestServices(TestCase):
    def test_disactivate_expired_subscriptions(self):
        SubscriptionFactory.create_batch(4, term_end=ddt.datetime.now() - ddt.timedelta(days=1))
        SubscriptionFactory.create_batch(2, term_end=ddt.datetime.now())

        with self.assertLogs('main.services', level='INFO') as cm:
            disactivated = disactivate_expired_subscriptions()
        self.assertEqual(4, disactivated)
        self.assertGreater(len(cm.output), 0)
