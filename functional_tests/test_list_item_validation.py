from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):

		# User goes to the home page and accidentally submits an
		# empty list item (hits enter with no text)
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

		# The home page refreshes, and there is an error message saying 
		# list items cannot be blank
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))

		# User submits a normal list item
		self.browser.find_element_by_id('id_new_item').send_keys('Finish these lists')
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Finish these lists')

		# User makes another mistake and submits another empty list item
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
		# The home page refreshes, and there is an error message saying 
		# list items cannot be blank
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))

		# User corrects mistake and inputs new list item
		self.browser.find_element_by_id('id_new_item').send_keys('Finish this test')
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Finish these lists')
		self.wait_for_row_in_list_table('2: Finish this test')

		self.fail('write me!')
