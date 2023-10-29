
from functools import wraps
from django.http import HttpResponseForbidden

def or_permission_required(*permissions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if any(request.user.has_perm(permission) for permission in permissions):
                
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Permission denied")

        return _wrapped_view

    return decorator
