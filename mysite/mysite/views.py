from django.shortcuts import render

def index(request):
    """
    Handles the index page for authenticated and non-authenticated user
    """
    if request.user.is_authenticated:
        return render(request, "mysite/dashboard.html", {})
    else:
        return render(request, "mysite/index.html", {})
