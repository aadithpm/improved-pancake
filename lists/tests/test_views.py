# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import skip

from django.test import TestCase
from django.utils.html import escape
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


class HomePageTest(TestCase):

    def test_canary(self):
        self.assertTrue(True)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other item 1', list=other_list)
        Item.objects.create(text='other item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'other item 1')
        self.assertNotContains(response, 'other item 2')

    def test_can_save_a_POST_request_to_an_existing_item(self):
        first_list = List.objects.create()

        self.client.post(
            f'/lists/{first_list.id}/',
            data={'text': 'Item for existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Item for existing list')
        self.assertEqual(new_item.list, first_list)

    def test_POST_redirects_to_list_view(self):
        first_list = List.objects.create()

        response = self.client.post(
            f'/lists/{first_list.id}/',
            data={'text': 'Item for existing list'}
        )

        self.assertRedirects(response, f'/lists/{first_list.id}/')

    def test_passes_correct_list_to_template(self):
        first_list = List.objects.create()
        response = self.client.get(f'/lists/{first_list.id}/')
        self.assertEqual(response.context['list'], first_list)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    @skip
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        print(response.content)
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    @skip
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
