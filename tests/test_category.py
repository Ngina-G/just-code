import unittest
from app.models import Category
from app import db

class CategoryTest(unittest.TestCase):
    """
        Test class to test the behaviour of the Categryategory
    """
    def setUp(self):
        """
            Set up method that will run before every test
        """
        self.new_category= Category('Coding')

    def test_initialization(self):
        self.assertEquals(self.new_category.name, 'Coding')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_category, Category))

    def test_save_category(self):
        self.new_category.save_category()
        self.assertTrue(len(Category.query.all())>0)
