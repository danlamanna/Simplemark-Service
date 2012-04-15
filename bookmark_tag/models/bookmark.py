from django.db import models

class Bookmark(models.Model):
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    title      = models.CharField(max_length=255)   
    url        = models.URLField(max_length=200, unique=True)  
    read       = models.BooleanField(default=1)

    def __unicode__(self):
        return self.title

    def __repr__(self):
        from pprint import pformat

        return "<Bookmark %s>" % pformat ({ "created_at": self.created_at,
                                            "title":      self.title,
                                            "url":        self.url,
                                            "read":       self.read,
                                            "tags":       self.get_tags() })

    """ Returns created_at in the form of a UNIX timestamp. """
    def created_timestamp(self):
        return self.created_at.strftime('%s')

    """ Adds a tag to the bookmark, creates it if it doesn't already exist. """
    def add_tag(self, name):
        from string import strip
        from tag    import Tag
        from bookmark_tag import Bookmark_Tag

        if (not self.id):
            self.save()

        new_tag_obj, created = Tag.objects.get_or_create(name=name.strip())

        Bookmark_Tag.objects.create(bookmark_id=self.id, tag_id=new_tag_obj.id)

    """ Gets all tags related to the current bookmark, returns them in a list,
    optional arg of set_on_obj which will store the list in self.tags """
    def get_tags(self, set_on_obj=False):
        from tag import Tag
        from bookmark_tag import Bookmark_Tag
        
        related_bookmark_tag_ids = Bookmark_Tag.objects.filter(bookmark=self).values('tag')
        related_tags             = Tag.objects.filter(pk__in=related_bookmark_tag_ids)

        if (set_on_obj):
            self.tags = related_tags

        return list(related_tags.values())

    class Meta:
        app_label = 'bookmark_tag'
        db_table  = 'bookmark'
