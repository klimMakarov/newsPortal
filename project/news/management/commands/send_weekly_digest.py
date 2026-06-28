import logging
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from news.models import Post, Category
from django.core.mail import EmailMultiAlternatives



logger = logging.getLogger(__name__)

def send_digest():
    now = timezone.now()
    week_ago = now - timedelta(days=7)

    categories = Category.objects.prefetch_related('subscribers').all()

    for category in categories:
        subscribers = [u for u in category.subscribers.all() if u.email]
        if not subscribers:
            continue

        new_posts = (Post.objects.filter(category=category, created__gte=week_ago).distinct())

        if not new_posts:
            continue

        for user in subscribers:
            html_content = render_to_string(
                'email_weekly.html',
                {
                    'user': user,
                    'category': category,
                    'posts': new_posts
                }
            )

            from_email = 'makarendan-yan@yandex.ru'
            subject = f'Дайджест: новые статьи в разделе «{category.name}»'

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=from_email,
                to=[user.email],
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            logger.info('Sent digest to %s for category %s', user.email, category.name)



class Command(BaseCommand):
    help = 'Send weekly digest of new articles to subscribers'

    def handle(self, *args, **options):
        logger.info('Starting weekly digest send')
        send_digest()
        logger.info('Weekly digest send completed')