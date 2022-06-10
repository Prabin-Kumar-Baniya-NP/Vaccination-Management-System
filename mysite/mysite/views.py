from django.shortcuts import render


def index(request):
    """
    Handles the index page for authenticated and non-authenticated user
    """
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {})
    else:
        return render(request, "index.html", {})
