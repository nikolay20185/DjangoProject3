from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from .models import CodeSnippet, Tag, ProgrammingLanguage, Comment, Like
from .forms import CodeSnippetForm, CommentForm, SnippetSearchForm


def snippet_list(request):
    """
    Display a list of all published snippets.
    """
    snippets = CodeSnippet.objects.filter(is_published=True)
    languages = ProgrammingLanguage.objects.all()
    popular_tags = Tag.objects.all()[:15]
    search_form = SnippetSearchForm()
    
    context = {
        'snippets': snippets,
        'languages': languages,
        'popular_tags': popular_tags,
        'search_form': search_form,
    }
    return render(request, 'library/snippet_list.html', context)


def snippet_list_by_tag(request, tag_slug):
    """
    Display snippets filtered by tag.
    """
    tag = get_object_or_404(Tag, slug=tag_slug)
    snippets = CodeSnippet.objects.filter(tags=tag, is_published=True)
    
    context = {
        'tag': tag,
        'snippets': snippets,
    }
    return render(request, 'library/snippet_list_by_tag.html', context)


def snippet_list_by_language(request, language_slug):
    """
    Display snippets filtered by programming language.
    """
    language = get_object_or_404(ProgrammingLanguage, slug=language_slug)
    snippets = CodeSnippet.objects.filter(language=language, is_published=True)
    
    context = {
        'language': language,
        'snippets': snippets,
    }
    return render(request, 'library/snippet_list_by_language.html', context)


def snippet_search(request):
    """
    Search for snippets based on query and filters.
    """
    form = SnippetSearchForm(request.GET)
    snippets = CodeSnippet.objects.filter(is_published=True)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        language = form.cleaned_data.get('language')
        
        if query:
            snippets = snippets.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(code__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        
        if language:
            snippets = snippets.filter(language=language)
    
    context = {
        'form': form,
        'snippets': snippets,
    }
    return render(request, 'library/snippet_search.html', context)


def snippet_detail(request, slug):
    """
    Display a single snippet with comments.
    """
    snippet = get_object_or_404(CodeSnippet, slug=slug, is_published=True)
    comments = snippet.comments.filter(is_active=True)
    comment_form = CommentForm()
    
    # Increment view count
    snippet.views_count += 1
    snippet.save(update_fields=['views_count'])
    
    # Check if user has liked this snippet
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = snippet.likes.filter(user=request.user).exists()
    
    # Get similar snippets
    similar_snippets = CodeSnippet.objects.filter(
        language=snippet.language,
        is_published=True
    ).exclude(id=snippet.id)[:4]
    
    context = {
        'snippet': snippet,
        'comments': comments,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
        'similar_snippets': similar_snippets,
    }
    return render(request, 'library/snippet_detail.html', context)


@login_required
def snippet_create(request):
    """
    Create a new code snippet.
    """
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            snippet.save()
            form.save_m2m()  # Save the tags
            messages.success(request, 'Сниппет успешно создан!')
            return redirect('library:snippet_detail', slug=snippet.slug)
    else:
        form = CodeSnippetForm()
    
    context = {
        'form': form,
        'title': 'Создать новый сниппет'
    }
    return render(request, 'library/snippet_form.html', context)


@login_required
def snippet_edit(request, slug):
    """
    Edit an existing code snippet.
    """
    snippet = get_object_or_404(CodeSnippet, slug=slug)
    
    # Check if user is the author
    if snippet.author != request.user:
        messages.error(request, 'У вас нет прав на редактирование этого сниппета.')
        return redirect('library:snippet_detail', slug=snippet.slug)
    
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сниппет успешно обновлен!')
            return redirect('library:snippet_detail', slug=snippet.slug)
    else:
        # Prepare initial tags data as comma-separated string
        initial_tags = ', '.join([tag.name for tag in snippet.tags.all()])
        form = CodeSnippetForm(instance=snippet, initial={'tags': initial_tags})
    
    context = {
        'form': form,
        'title': 'Редактировать сниппет',
        'snippet': snippet
    }
    return render(request, 'library/snippet_form.html', context)


@login_required
def snippet_delete(request, slug):
    """
    Delete a code snippet.
    """
    snippet = get_object_or_404(CodeSnippet, slug=slug)
    
    # Check if user is the author
    if snippet.author != request.user:
        messages.error(request, 'У вас нет прав на удаление этого сниппета.')
        return redirect('library:snippet_detail', slug=snippet.slug)
    
    if request.method == 'POST':
        snippet.delete()
        messages.success(request, 'Сниппет успешно удален!')
        return redirect('library:snippet_list')
    
    return render(request, 'library/snippet_confirm_delete.html', {'snippet': snippet})


@login_required
@require_POST
def snippet_like(request, slug):
    """
    Like or unlike a snippet.
    """
    snippet = get_object_or_404(CodeSnippet, slug=slug, is_published=True)
    like, created = Like.objects.get_or_create(snippet=snippet, user=request.user)
    
    if not created:
        # User already liked, so unlike
        like.delete()
        snippet.likes_count = max(0, snippet.likes_count - 1)
        liked = False
    else:
        # New like
        snippet.likes_count += 1
        liked = True
    
    snippet.save(update_fields=['likes_count'])
    
    if request.is_ajax():
        return JsonResponse({
            'liked': liked,
            'likes_count': snippet.likes_count
        })
    else:
        return redirect('library:snippet_detail', slug=snippet.slug)


@login_required
def snippet_download(request, slug):
    """
    Download a snippet as a file.
    """
    snippet = get_object_or_404(CodeSnippet, slug=slug, is_published=True)
    
    # Increment download count
    snippet.downloads_count += 1
    snippet.save(update_fields=['downloads_count'])
    
    # Determine file extension based on language
    extension = 'txt'
    if snippet.language:
        if 'python' in snippet.language.name.lower():
            extension = 'py'
        elif 'javascript' in snippet.language.name.lower():
            extension = 'js'
        elif 'html' in snippet.language.name.lower():
            extension = 'html'
        elif 'css' in snippet.language.name.lower():
            extension = 'css'
        elif 'java' in snippet.language.name.lower():
            extension = 'java'
        elif 'c#' in snippet.language.name.lower():
            extension = 'cs'
        elif 'php' in snippet.language.name.lower():
            extension = 'php'
    
    # Create response with code content
    response = HttpResponse(snippet.code, content_type='text/plain')
    filename = f"{slugify(snippet.title)}.{extension}"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required
@require_POST
def snippet_comment(request, slug):
    """
    Add a comment to a snippet.
    """
    snippet = get_object_or_404(CodeSnippet, slug=slug, is_published=True)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.snippet = snippet
        comment.author = request.user
        comment.save()
        messages.success(request, 'Комментарий добавлен!')
    
    return redirect('library:snippet_detail', slug=snippet.slug)


@login_required
def comment_delete(request, comment_id):
    """
    Delete a comment.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user is the author or snippet owner
    if comment.author != request.user and comment.snippet.author != request.user:
        messages.error(request, 'У вас нет прав на удаление этого комментария.')
        return redirect('library:snippet_detail', slug=comment.snippet.slug)
    
    if request.method == 'POST':
        snippet_slug = comment.snippet.slug
        comment.delete()
        messages.success(request, 'Комментарий удален!')
        return redirect('library:snippet_detail', slug=snippet_slug)
    
    return render(request, 'library/comment_confirm_delete.html', {'comment': comment}) 