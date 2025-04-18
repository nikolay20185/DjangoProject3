from django.shortcuts import render
from codeswap.apps.library.models import CodeSnippet


def home(request):
    """
    Home page view.
    """
    # Get most popular code snippets for display
    popular_snippets = CodeSnippet.objects.filter(
        is_published=True).order_by('-views_count', '-likes_count')[:4]
    
    context = {
        'popular_snippets': popular_snippets
    }
    return render(request, 'core/home.html', context)


def about(request):
    """
    About page view.
    """
    return render(request, 'core/about.html') 