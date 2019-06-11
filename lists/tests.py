# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase


class SmokeTest(TestCase):

    def test_canary(self):
        self.assertTrue(True)

    def test_bad_math(self):
        self.assertEqual(1 + 1, 3)
