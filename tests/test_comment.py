import unittest
from app.models import Comment
from app import db

class CommentTest(unittest.TestCase):
    """
        Test class to test the behaviour of the Comment class
    """
    def setUp(self):
        """
            Set up method that will run before every test
        """
        self.new_comment= Comment('Consistency is key',1,1)

    def test_initialization(self):
        self.assertEquals(self.new_comment.opinion, 'Consistency is key')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)


    def test_get_comments_by_post_id(self):
        got_comments = Comment.get_comments(1)
        self.assertFalse(len(got_comments) >= 1)
