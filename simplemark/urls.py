from django.conf.urls import patterns, include, url

urlpatterns = patterns('bookmark_tag.views',
                       # API
                       url(r'^api/bookmarks$',    'get_bookmarks'),
                       url(r'^api/bookmark/add$', 'add_bookmark'),

                       
)
