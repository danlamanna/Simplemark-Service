from django.db import models

from bookmark import Bookmark
from tag      import Tag

class Bookmark_Tag(models.Model):
    bookmark = models.ForeignKey(Bookmark)
    tag      = models.ForeignKey(Tag)

    class Meta:
        app_label = 'bookmark_tag'
        db_table  = 'bookmark_tag'
