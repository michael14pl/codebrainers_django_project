from django.test import TestCase

# Create your tests here.

class BarTest(TestCase):
	def test_false(self):
		self.assertFalse(False)
