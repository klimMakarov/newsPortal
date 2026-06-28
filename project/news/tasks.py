from celery import shared_task
import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from django.utils import timezone
from datetime import timedelta



# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")


# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)


@shared_task
def send_post_notification_to_subscribers(post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return
    
    users = set()
    for category in post.category.all():
        for user in category.subscribers.all():
            if user.email:
                users.add(user)

    if not users:
        return

    preview_text = post.text if len(post.text) < 50 else post.text[:50]

    for user in users:
        categories_names = ', '.join(c.name for c in post.category.all())
        html_content = render_to_string(
            'email_notification.html',
            {
                'post': post,
                'user': user,
                'categories_names': categories_names,
                'preview_text': preview_text,
            }
        )

        msg = EmailMultiAlternatives(
            subject=post.title,
            from_email='makarendan-yan@yandex.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def send_weekly_digest():
    now = timezone.now()
    week_ago = now - timedelta(days=7)

    categories = Category.objects.prefetch_related('subscribers').all()

    for category in categories:
        subscribers = [u for u in category.subscribers.all() if u.email]
        if not subscribers:
            continue

        new_posts = Post.objects.filter(
            category=category,
            created__gte=week_ago
        ).distinct()

        if not new_posts:
            continue

        for user in subscribers:
            html_content = render_to_string(
                'email_weekly.html',
                {
                    'user': user,
                    'category': category,
                    'posts': new_posts,
                }
            )

            subject = f'Дайджест: новые статьи в разделе «{category.name}»'
            from_email = 'makarendan-yan@yandex.ru'

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=from_email,
                to=[user.email],
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()