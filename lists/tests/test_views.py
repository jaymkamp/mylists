from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
import re

from lists.models import Item, List
from lists.views import home_page

class HomePageTest(TestCase):

	#help function for removing csrf token from html
	#need to remove csrf token before comparing html
	def remove_csrf(self,html_code):
		csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
		return re.sub(csrf_regex, '', html_code)

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def assertEqualExceptCSRF(self, html_code1, html_code2):
		return self.assertEqual(
			self.remove_csrf(html_code1),
			self.remove_csrf(html_code2)
		)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html', request=request)
		self.assertEqualExceptCSRF(response.content.decode(), expected_html)


class NewListTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)

		self.assertEqual(Item.objects.count(),1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		new_list = List.objects.first()
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

class NewItemTest(TestCase):

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			'/lists/%d/add_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(),1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/lists/%d/add_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))


class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_all_items(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)
		
		response = self.client.get('/lists/%d/' % (correct_list.id,))

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')

	def test_pass_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)

