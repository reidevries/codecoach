from saunter.testcase.webdriver import SaunterTestCase

from pages.google import GooglePage
from pages.walmart import WalmartPage

from providers.txt_provider import TXTProvider

import collections
import pytest
import json


class TestMain(SaunterTestCase):
    @pytest.marks('shallow')
    def test_control(self):

        results = []

        # Get provider data
        t = TXTProvider('product_urls.txt')

        # Load the control preview url
        w = WalmartPage(self.driver)
        w.open_control_preview_url()

        for url in t.data:

            # Execute the Google redirect
            g = GooglePage(self.driver)
            g.redirect(url)

            # Get the list of recommendations
            recs = w.get_control_recommendations()

            # Append recommendation data to results
            d = collections.OrderedDict()
            d['product_id'] = url.split('/')[-1]
            d['url'] = url
            d['num_recommendations'] = len(recs)
            d['recommendations'] = recs
            results.append(d)

            # Save screenshot to disk
            #w.save_screenshot("control_{0}".format(d['product_id']))

        with open("results/control.json", "w") as f:
            f.write(json.dumps(results, sort_keys=False))

    @pytest.marks('shallow')
    def test_variant(self):

        results = []

        # Get provider data
        t = TXTProvider('product_urls.txt')

        # Load the variant preview url and accept the alert
        w = WalmartPage(self.driver)
        w.open_variant_preview_url()
        w.accept_alert()

        for url in t.data:

            # Execute the Google redirect
            g = GooglePage(self.driver)
            g.redirect(url)

            # Accept the alerts
            w.accept_alert()
            w.accept_alert()
            w.accept_alert()

            # Get the list of recommendations
            recs = w.get_variant_recommendations()

            # Append recommendation data to results
            d = collections.OrderedDict()
            d['product_id'] = url.split('/')[-1]
            d['url'] = url
            d['num_recommendations'] = len(recs)
            d['recommendations'] = recs
            results.append(d)

            # Save screenshot to disk
            #w.save_screenshot("control_{0}".format(d['product_id']))

        with open("results/variant.json", "w") as f:
            f.write(json.dumps(results, sort_keys=False))
