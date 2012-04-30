from bookmark_tag.models import Bookmark, Tag, Bookmark_Tag

from django.shortcuts import render_to_response, redirect

from django.http import HttpRequest, HttpResponse

# ^bookmarks/all
def all_bookmarks(request):
    all_bookmarks = Bookmark.objects.all().order_by('created_at')

    bookmark_response = []

    for bookmark in all_bookmarks:
        resp = { "id":         bookmark.id,
                 "created_at": bookmark.created_timestamp(),
                 "title":      bookmark.title,
                 "url":        bookmark.url,
                 "read":       bookmark.read,
                 "tags":       bookmark.get_tags() }

        resp["tag_names"]  = [ tag["name"] for tag in resp["tags"] ]
        resp["tag_counts"] = bookmark.get_tag_name_and_occurrences() 

        bookmark_response.append(resp)

    return render_to_response("all_bookmarks.djhtml", { "bookmarks": bookmark_response })
            
# ^bookmark/delete/(.*)$
def delete_bookmark(request, bookmark_id):
    Bookmark.objects.get(id=bookmark_id).delete()

    return redirect(request.META.get('HTTP_REFERER', None))

# ^bookmarks/new$
def new_bookmark(request):
    from django.forms.models import modelformset_factory
    
    BookmarkFormSet = modelformset_factory(Bookmark)

    if request.method == 'POST':
        formset = BookmarkFormSet(request.POST)

        if formset.is_valid():
            formset.save()
    else:
        formset = BookmarkFormSet(queryset=Bookmark.objects.none())
    
        return render_to_response("new_bookmark.djhtml", { "formset": formset })
