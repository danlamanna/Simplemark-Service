from bookmark_tag.models import Bookmark, Tag, Bookmark_Tag

from django.http import HttpRequest, HttpResponse

from django.views.decorators.csrf import csrf_exempt

from django.utils.simplejson import dumps

from datetime import datetime

from string import strip

#from ajax import ajax_error

# ^api/bookmarks
def get_bookmarks(request):
#    return HttpResponse(ajax_error())
    all_bookmarks = Bookmark.objects.all()    

    bookmark_response = []

    for bookmark in all_bookmarks:
        resp = { "id":         bookmark.id,
                 "created_at": bookmark.created_at.strftime('%s'),
                 "title":      bookmark.title,
                 "url":        bookmark.url,
                 "read":       bookmark.read,
                 "tags":       bookmark.get_tags() }

        bookmark_response.append(resp)

    return HttpResponse(dumps(bookmark_response))

# ^api/bookmark/add
@csrf_exempt
def add_bookmark(request):
    has_required_fields = ("title" in request.POST and "url" in request.POST)
    has_tags            = ("tags" in request.POST)
    
    if (not has_required_fields):
        return HttpResponse('0')
    elif (has_tags):
        tags = request.POST['tags'].split(',')
        tags = [tag.strip() for tag in tags]

    bookmark_obj, created = Bookmark.objects.get_or_create(title=request.POST['title'], url=request.POST['url'])
    
    if (has_tags):
        related_tags = []
        [related_tags.append(Tag.objects.get_or_create(name=tag_name)[0]) for tag_name in tags]

        for tag_obj in related_tags:
            if (not Bookmark_Tag.objects.filter(bookmark=bookmark_obj, tag=tag_obj).count()):
                bookmark_tag = Bookmark_Tag(bookmark=bookmark_obj, tag=tag_obj)
                bookmark_tag.save()

    return HttpResponse('1')
