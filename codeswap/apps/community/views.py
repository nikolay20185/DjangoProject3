from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.auth.models import User
from .models import Topic, Discussion, Reply, Notification
from .forms import DiscussionForm, ReplyForm, DiscussionSearchForm


def topic_list(request):
    """
    Display a list of all forum topics.
    """
    topics = Topic.objects.annotate(discussions_count=Count('discussions'))
    search_form = DiscussionSearchForm()
    
    context = {
        'topics': topics,
        'search_form': search_form,
    }
    return render(request, 'community/topic_list.html', context)


@login_required
def topic_create(request):
    """
    Create a new topic (admin only).
    """
    # Check if user is staff or superuser
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'У вас нет прав на создание разделов форума.')
        return redirect('community:topic_list')
    
    if request.method == 'POST':
        # В этом месте обычно была бы обработка формы TopicForm
        # Но так как у нас её нет, для простоты создадим топик напрямую
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if name:
            Topic.objects.create(name=name, description=description)
            messages.success(request, 'Раздел форума создан!')
            return redirect('community:topic_list')
        else:
            messages.error(request, 'Имя раздела обязательно для заполнения.')
    
    return render(request, 'community/topic_form.html')


def topic_detail(request, slug):
    """
    Display a topic with its discussions.
    """
    topic = get_object_or_404(Topic, slug=slug)
    discussions = Discussion.objects.filter(topic=topic)
    
    # Add pinned discussions at the top
    pinned_discussions = discussions.filter(is_pinned=True)
    regular_discussions = discussions.filter(is_pinned=False)
    
    context = {
        'topic': topic,
        'pinned_discussions': pinned_discussions,
        'regular_discussions': regular_discussions,
    }
    return render(request, 'community/topic_detail.html', context)


def discussion_detail(request, slug):
    """
    Display a discussion with its replies.
    """
    discussion = get_object_or_404(Discussion, slug=slug)
    replies = discussion.replies.all()
    
    # Increment view count
    discussion.views_count += 1
    discussion.save(update_fields=['views_count'])
    
    # Find the solution if exists
    solution = replies.filter(is_solution=True).first()
    
    # Prepare reply form if the discussion is open
    reply_form = None
    if not discussion.is_closed and request.user.is_authenticated:
        if request.method == 'POST':
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.discussion = discussion
                reply.author = request.user
                reply.save()
                
                # Create notification for discussion author if it's not the same user
                if discussion.author != request.user:
                    Notification.objects.create(
                        user=discussion.author,
                        notification_type='reply',
                        sender=request.user,
                        discussion=discussion,
                        reply=reply,
                        message=f'Новый ответ в вашем обсуждении "{discussion.title}"'
                    )
                
                messages.success(request, 'Ответ добавлен!')
                return redirect('community:discussion_detail', slug=discussion.slug)
        else:
            reply_form = ReplyForm()
    
    context = {
        'discussion': discussion,
        'replies': replies,
        'reply_form': reply_form,
        'solution': solution,
    }
    return render(request, 'community/discussion_detail.html', context)


@login_required
def discussion_create(request):
    """
    Create a new discussion.
    """
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.save()
            messages.success(request, 'Обсуждение создано!')
            return redirect('community:discussion_detail', slug=discussion.slug)
    else:
        # Pre-select topic if provided in GET parameters
        initial = {}
        topic_id = request.GET.get('topic')
        if topic_id:
            try:
                initial['topic'] = Topic.objects.get(id=topic_id)
            except Topic.DoesNotExist:
                pass
        
        form = DiscussionForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Создать обсуждение'
    }
    return render(request, 'community/discussion_form.html', context)


@login_required
def discussion_edit(request, slug):
    """
    Edit an existing discussion.
    """
    discussion = get_object_or_404(Discussion, slug=slug)
    
    # Check if user is the author
    if discussion.author != request.user:
        messages.error(request, 'У вас нет прав на редактирование этого обсуждения.')
        return redirect('community:discussion_detail', slug=discussion.slug)
    
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Обсуждение обновлено!')
            return redirect('community:discussion_detail', slug=discussion.slug)
    else:
        form = DiscussionForm(instance=discussion)
    
    context = {
        'form': form,
        'title': 'Редактировать обсуждение',
        'discussion': discussion
    }
    return render(request, 'community/discussion_form.html', context)


@login_required
def discussion_delete(request, slug):
    """
    Delete a discussion.
    """
    discussion = get_object_or_404(Discussion, slug=slug)
    
    # Check if user is the author
    if discussion.author != request.user:
        messages.error(request, 'У вас нет прав на удаление этого обсуждения.')
        return redirect('community:discussion_detail', slug=discussion.slug)
    
    if request.method == 'POST':
        topic = discussion.topic
        discussion.delete()
        messages.success(request, 'Обсуждение удалено!')
        return redirect('community:topic_detail', slug=topic.slug)
    
    return render(request, 'community/discussion_confirm_delete.html', {'discussion': discussion})


@login_required
def discussion_close(request, slug):
    """
    Close or reopen a discussion.
    """
    discussion = get_object_or_404(Discussion, slug=slug)
    
    # Check if user is the author
    if discussion.author != request.user:
        messages.error(request, 'У вас нет прав на закрытие/открытие этого обсуждения.')
        return redirect('community:discussion_detail', slug=discussion.slug)
    
    discussion.is_closed = not discussion.is_closed
    discussion.save(update_fields=['is_closed'])
    
    status = 'закрыто' if discussion.is_closed else 'открыто'
    messages.success(request, f'Обсуждение {status}!')
    
    return redirect('community:discussion_detail', slug=discussion.slug)


@login_required
def discussion_pin(request, slug):
    """
    Pin or unpin a discussion (admin only).
    """
    discussion = get_object_or_404(Discussion, slug=slug)
    
    # Check if user is staff or superuser
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'У вас нет прав на закрепление/открепление обсуждений.')
        return redirect('community:discussion_detail', slug=discussion.slug)
    
    discussion.is_pinned = not discussion.is_pinned
    discussion.save(update_fields=['is_pinned'])
    
    status = 'закреплено' if discussion.is_pinned else 'откреплено'
    messages.success(request, f'Обсуждение {status}!')
    
    return redirect('community:discussion_detail', slug=discussion.slug)


@login_required
def reply_edit(request, pk):
    """
    Edit a reply.
    """
    reply = get_object_or_404(Reply, pk=pk)
    
    # Check if user is the author
    if reply.author != request.user:
        messages.error(request, 'У вас нет прав на редактирование этого ответа.')
        return redirect('community:discussion_detail', slug=reply.discussion.slug)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ответ обновлен!')
            return redirect('community:discussion_detail', slug=reply.discussion.slug)
    else:
        form = ReplyForm(instance=reply)
    
    context = {
        'form': form,
        'title': 'Редактировать ответ',
        'reply': reply
    }
    return render(request, 'community/reply_form.html', context)


@login_required
def reply_delete(request, pk):
    """
    Delete a reply.
    """
    reply = get_object_or_404(Reply, pk=pk)
    
    # Check if user is the author or discussion owner
    if reply.author != request.user and reply.discussion.author != request.user:
        messages.error(request, 'У вас нет прав на удаление этого ответа.')
        return redirect('community:discussion_detail', slug=reply.discussion.slug)
    
    if request.method == 'POST':
        discussion_slug = reply.discussion.slug
        reply.delete()
        messages.success(request, 'Ответ удален!')
        return redirect('community:discussion_detail', slug=discussion_slug)
    
    return render(request, 'community/reply_confirm_delete.html', {'reply': reply})


@login_required
def reply_mark_solution(request, pk):
    """
    Mark a reply as the solution to the discussion.
    """
    reply = get_object_or_404(Reply, pk=pk)
    
    # Check if user is the discussion author
    if reply.discussion.author != request.user:
        messages.error(request, 'Только автор обсуждения может отметить ответ как решение.')
        return redirect('community:discussion_detail', slug=reply.discussion.slug)
    
    # Clear any existing solution
    Reply.objects.filter(discussion=reply.discussion, is_solution=True).update(is_solution=False)
    
    # Mark this reply as the solution
    reply.is_solution = True
    reply.save(update_fields=['is_solution'])
    
    # Create notification for reply author
    if reply.author != request.user:
        Notification.objects.create(
            user=reply.author,
            notification_type='solution',
            sender=request.user,
            discussion=reply.discussion,
            reply=reply,
            message=f'Ваш ответ был отмечен как решение в "{reply.discussion.title}"'
        )
    
    messages.success(request, 'Ответ отмечен как решение!')
    return redirect('community:discussion_detail', slug=reply.discussion.slug)


def user_discussions(request, username):
    """
    Display discussions created by a user.
    """
    user = get_object_or_404(User, username=username)
    discussions = Discussion.objects.filter(author=user)
    
    context = {
        'profile_user': user,
        'discussions': discussions,
    }
    return render(request, 'community/user_discussions.html', context)


def user_replies(request, username):
    """
    Display replies created by a user.
    """
    user = get_object_or_404(User, username=username)
    replies = Reply.objects.filter(author=user)
    
    context = {
        'profile_user': user,
        'replies': replies,
    }
    return render(request, 'community/user_replies.html', context)


@login_required
def notification_list(request):
    """
    Display notifications for the current user.
    """
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    
    # Mark as read
    if request.GET.get('mark_read'):
        notification_id = request.GET.get('mark_read')
        Notification.objects.filter(id=notification_id, user=request.user).update(is_read=True)
        return redirect('community:notification_list')
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'community/notification_list.html', context)


@login_required
def notification_mark_all_read(request):
    """
    Mark all notifications as read.
    """
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'Все уведомления отмечены как прочитанные.')
    return redirect('community:notification_list')


def discussion_search(request):
    """
    Search for discussions.
    """
    form = DiscussionSearchForm(request.GET)
    discussions = Discussion.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        topic = form.cleaned_data.get('topic')
        
        if query:
            discussions = discussions.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )
        
        if topic:
            discussions = discussions.filter(topic=topic)
    
    context = {
        'form': form,
        'discussions': discussions,
    }
    return render(request, 'community/discussion_search.html', context) 