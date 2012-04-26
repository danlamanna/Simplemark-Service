from bookmark_tag.models import Bookmark, Tag, Bookmark_Tag

from helpers.ajax import ajax_error, ajax_success

from django.http import HttpRequest, HttpResponse

from django.views.decorators.csrf import csrf_exempt

from django.utils.simplejson import dumps

from datetime import datetime

from string import strip

# ^api/bookmarks
def get_bookmarks(request):
    all_bookmarks = Bookmark.objects.all()    

    bookmark_response = []

    for bookmark in all_bookmarks:
        resp = { "id":         bookmark.id,
                 "created_at": bookmark.created_timestamp(),
                 "title":      bookmark.title,
                 "url":        bookmark.url,
                 "read":       bookmark.read,
                 "tags":       bookmark.get_tags() }

        bookmark_response.append(resp)

    return HttpResponse(dumps(ajax_success(bookmark_response)))

# ^api/bookmark/add
@csrf_exempt
def add_bookmark(request):
    has_required_fields = ("title" in request.POST and "url" in request.POST)
    has_tags            = ("tags" in request.POST)
    
    if (not has_required_fields):
        return HttpResponse(dumps(ajax_error('Missing required fields.')))
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

    return HttpResponse(dumps(ajax_success()))

# ^api/tags
def get_tags(request):
    all_tags = Tag.objects.all()

    tag_response = []

    for tag in all_tags:
        resp = { "id":    tag.id,
                 "name":  tag.name,
                 "count": tag.num_occurrences() }

        tag_response.append(resp)

    return HttpResponse(dumps(ajax_success(tag_response)))

# ^api/tags-like/(.*)
# @needs_tests
def get_tags_like(request, partial_tag):
    tags_like = Tag.objects.filter(name__startswith=partial_tag)

    tag_response = []

    for tag in tags_like:
        resp = { "id":    tag.id,
                 "name":  tag.name,
                 "count": tag.num_occurrences() }

        tag_response.append(resp)

    return HttpResponse(dumps(ajax_success(tag_response)))

# ^api/tag/(.*)
def get_tag(request, tag_name):
    try:
        tag_obj = Tag.objects.get(name=tag_name)
    except Tag.DoesNotExist:
        return HttpResponse(dumps(ajax_success()))

    return HttpResponse(dumps(ajax_success(tag_obj.get_bookmarks())))
