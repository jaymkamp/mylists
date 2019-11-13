from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):

		self.fail('write me!')
