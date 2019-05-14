from django.test import TestCase

from wykop.posts.models import Post, Vote
from wykop.accounts.models import User

# Create your tests here.

class BarTest(TestCase):
	def test_false(self):
		self.assertFalse(False)

	def test_votes(self):
		user1 = User.objects.create(username="Alice")
		user2 = User.objects.create(username="Bob")
		post = Post.objects.create(author=user1)
		vote1 = Vote.objects.create(user=user1, post=post, value=1)
		vote2 = Vote.objects.create(user=user2, post=post, value=1)
		
		self.assertEquals(Post.objects.get(id=1).score, 2)
