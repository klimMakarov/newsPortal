from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Post
from django.template.loader import render_to_string
from .tasks import send_post_notification_to_subscribers



# @receiver(m2m_changed, sender=Post.category.through)
# def notify_subscribers(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         post = instance
#         users = set()
#         for category in post.category.all():
#             for user in category.subscribers.all():
#                 if user.email:
#                     users.add(user)
        
#         if not users:
#             return
    
#         preview_text = post.text if len(post.text) < 50 else post.text[:50]
        
#         for user in users:
#             categories_names = ', '.join(c.name for c in post.category.all())
#             html_content = render_to_string(
#                 'email_notification.html',
#                 {
#                     'post': post,
#                     'user': user,
#                     'categories_names': categories_names,
#                     'preview_text': preview_text,
#                 }
#             )

#             msg = EmailMultiAlternatives(
#                 subject=f'{post.title}',
#                 from_email='makarendan-yan@yandex.ru',
#                 to=[user.email],
#             )

#             msg.attach_alternative(html_content, 'text/html')
#             msg.send()
        

@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        send_post_notification_to_subscribers.delay(post_id=instance.pk)