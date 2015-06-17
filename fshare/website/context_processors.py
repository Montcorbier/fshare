from website.models import FSUser


def storage(request):
    """
        Add storage space relative information to context:
        - limit of storage space as defined by the permission class
            of the user
        - free storage left

    """
    ctxt = dict()
    if not request.user.is_authenticated() or request.user.is_anonymous():
        return ctxt
    ctxt["storage_limit"] = FSUser.objects.get(user=request.user).permission.storage_limit
    #TODO add free space left
    return ctxt

