from bookmark_tag.models import Bookmark, Tag, Bookmark_Tag

from django.shortcuts import render_to_response

from django.http import HttpRequest, HttpResponse

# ^tags/all$
def all_tags(request):
    all_tags = Tag.objects.all()

    tag_response = []

    for tag in all_tags:
        resp = { "id": tag.id,
                 "name": tag.name,
                 "count": tag.num_occurrences(),
                 "bookmarks": tag.get_bookmarks() }

        tag_response.append(resp)

    return render_to_response("all_tags.djhtml", { "tags": tag_response,
                                                   "bookmark_count": Bookmark.objects.count() })

# ^tags/(.*)$
def single_tag(request, tag_name):
    try:
        tag_obj = Tag.objects.get(name=tag_name)
    except Tag.DoesNotExist:
        return render_to_response("single_tag_not_found.djhtml", { "tag_name": tag_name })

    return render_to_response("single_tag.djhtml", { "tag":       tag_obj,
                                                     "count":     tag_obj.num_occurrences(),
                                                     "bookmarks": tag_obj.get_bookmarks() })

    
