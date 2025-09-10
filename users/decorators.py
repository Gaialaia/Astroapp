from django.contrib import messages
from django.shortcuts import redirect

def user_not_auth(function=None):
    def deco(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect('showed chart')
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return deco(function)

    return deco


def user_is_superuser(function=None, redirect_url='/'):

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_superuser:
                messages.error(request, "You are not authorized to access this!")
                return redirect(redirect_url)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator