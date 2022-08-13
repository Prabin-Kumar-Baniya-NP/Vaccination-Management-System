from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


@cache_page(60 * 15)
@vary_on_cookie
def index(request):
    """
    Handles the index page for authenticated and non-authenticated user
    """
    if request.user.is_authenticated:
        return render(request, "mysite/dashboard.html", {})
    else:
        return render(request, "mysite/index.html", {})
