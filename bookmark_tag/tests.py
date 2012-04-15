from django.utils import unittest

from bookmark_tag.models import *

class BookmarkTestCase(unittest.TestCase):
    def setUp(self):
        self.test_bookmark = Bookmark.objects.create(title='Test Bookmark', url='http://google.com')
        self.test_bookmark.save()
        self.test_bookmark.add_tag('Test Tag')

    def tearDown(self):
        self.test_bookmark.delete()

    def test_default_read(self):
        self.assertEqual(self.test_bookmark.read, True)

    def test_add_tag(self):
        self.assertIs(Tag.objects.filter(name='Test Tag').count(), 1)

    def test_bookmark_tag_relation(self):
        self.assertIs(Bookmark_Tag.objects.filter(bookmark=self.test_bookmark).count(), 1)

class TagTestCase(unittest.TestCase):
    def setUp(self):
        self.bookmark_params_dict = { "title": "Another Test Bookmark",
                                      "url":   "http://foo.bar",
                                      "read":  False } 

        self.test_tag = Tag.objects.create(name='Another Test Tag')
        self.test_tag.add_bookmark(self.bookmark_params_dict)

    def tearDown(self):
        self.test_tag.delete()

    def test_add_bookmark(self):
        self.assertIs(Bookmark.objects.filter(title=self.bookmark_params_dict['title'],
                                              url=self.bookmark_params_dict['url'],
                                              read=self.bookmark_params_dict['read']).count(), 1)

    def test_num_occurrences(self):
        self.assertIs(self.test_tag.num_occurrences(), 1)

    def test_get_bookmarks(self):
        self.assertIs(len(self.test_tag.get_bookmarks()), 1)

    def test_tag_bookmark_relation(self):
        self.assertIs(Bookmark_Tag.objects.filter(tag=self.test_tag).count(), 1)
