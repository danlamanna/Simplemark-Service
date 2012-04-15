def ajax_success(data=[]):
    return { "success": True,
             "data":    data }

def ajax_error(message=None):
    return { "success": False,
             "message": message }
