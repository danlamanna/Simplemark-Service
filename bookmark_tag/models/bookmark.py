from django.db import models
from django.forms import ModelForm

class Bookmark(models.Model):
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    title      = models.CharField(max_length=255)   
    url        = models.URLField(max_length=200, unique=True)  
    read       = models.BooleanField(default=1)

    tags       = []

    def __unicode__(self):
        return self.title

    def __repr__(self):
        from pprint import pformat

        return "<Bookmark %s>" % pformat ({ "created_at": self.created_at,
                                            "title":      self.title,
                                            "url":        self.url,
                                            "read":       self.read,
                                            "tags":       self.tags })

    def save(self, *args, **kwargs):
        from urlparse import urlparse
        import re

        parsed_url = urlparse(self.url)

        # Does this have to be urlparse? Can we just remove anything before :// ?
        # Remove scheme ://
        self.url = self.url.replace(parsed_url.scheme + '://', '')
        
        # Remove www. and trailing slash
        self.url = re.sub(r'^www\.', '', self.url)
        self.url = re.sub(r'\/$',    '', self.url)

        super(Bookmark, self).save(*args, **kwargs)

        # Goes through each tag, adds self bookmark to it, saves the tag
        if (self.tags):
            from bookmark_tag import Bookmark_Tag

            for tag in self.tags:
                tag.save()
                rel = Bookmark_Tag(bookmark=self, tag=tag)
                rel.save()
    
    def delete(self, *args, **kwargs):
        from bookmark_tag import Bookmark_Tag

        Bookmark_Tag.objects.filter(bookmark=self).delete()

        super(Bookmark, self).delete(*args, **kwargs)

    def get_url(self):
        return "http://" + self.url

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

    def get_tag_name_and_occurrences(self):
        from tag import Tag
        from bookmark_tag import Bookmark_Tag

        name_and_occurrences = {}

        related_bookmark_tag_ids = Bookmark_Tag.objects.filter(bookmark=self).values('tag')
        related_tags             = list(Tag.objects.filter(pk__in=related_bookmark_tag_ids))

        for tag_obj in related_tags:
            name_and_occurrences[tag_obj.name] = tag_obj.num_occurrences()
            
        return name_and_occurrences        

    class Meta:
        app_label = 'bookmark_tag'
        db_table  = 'bookmark'

class BookmarkForm(ModelForm):
    class Meta:
        model  = Bookmark
        fields = { "title",
                   "url",
                   "read" }
