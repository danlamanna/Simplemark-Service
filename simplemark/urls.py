from django.conf.urls import patterns, include, url

urlpatterns = patterns('bookmark_tag.views',
                       # API
                       url(r'^api/bookmarks$',      'get_bookmarks'),
                       url(r'^api/bookmark/add$',   'add_bookmark'),
                       url(r'^api/tags$',           'get_tags'),
                       url(r'^api/tag/(.*)$',       'get_tag'),
                       url(r'^api/tags-like/(.*)$', 'get_tags_like'),

                       # Bookmark
                       url(r'^bookmarks/all$',        'all_bookmarks'),
                       url(r'^bookmarks/new$',         'new_bookmark'),
                       url(r'^bookmark/delete/(.*)$', 'delete_bookmark'),

                       # Tag
                       url(r'^tags/all$',           'all_tags'),
                       url(r'^tags/(.*)$',          'single_tag'),
)
