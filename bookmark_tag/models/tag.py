from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        from pprint import pformat

        return "<Tag %s>" % pformat({ "name": self.name })

    """ Adds/Relates a bookmark to the current tag, creates it if necessary. """
    def add_bookmark(self, params):
        from bookmark     import Bookmark
        from bookmark_tag import Bookmark_Tag

        if (not self.id):
            self.save()

        new_bookmark_obj, created = Bookmark.objects.get_or_create(title=params['title'],
                                                                   url=params['url'],
                                                                   read=params['read'])

        Bookmark_Tag.objects.create(bookmark=new_bookmark_obj, tag=self)

    class Meta:
        app_label = 'bookmark_tag'
        db_table  = 'tag'
