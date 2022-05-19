import unittest
from app.models import Post
from app import db

class PostTest(unittest.TestCase):
    """
        Test class to test the behaviour of the Post class
    """
    def setUp(self):
        self.new_post = Post(1,'Get started with Html', 'Html is pretty straight-forward and a great way to get your feet wet with coding.', 1)

    def test_initialization(self):
        self.assertEquals(self.new_post.title, 'Get started with Html')
        self.assertEquals(self.new_post.content, 'Html is pretty straight-forward and a great way to get your feet wet with coding.')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post, Post))

    def test_save_post(self):
        self.new_post.save_post()
        self.assertTrue(len(Post.query.all())>0)
