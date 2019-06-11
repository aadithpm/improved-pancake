# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import resolve
from django.test import TestCase
from lists.views import home_page


class SmokeTest(TestCase):

    def test_canary(self):
        self.assertTrue(True)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
