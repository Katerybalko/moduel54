from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Reply, ReplyStatus

@receiver(post_save, sender=Reply)
def notify_post_author_on_new_reply(sender, instance: Reply, created, **kwargs):
    if created:
        send_mail(
            subject='Новый отклик на ваше объявление',
            message=f'На ваше объявление "{instance.post.title}" пришёл новый отклик от {instance.author.username}.',
            from_email=None,
            recipient_list=[instance.post.author.email],
            fail_silently=True
        )

@receiver(pre_save, sender=Reply)
def notify_reply_author_on_status_change(sender, instance: Reply, **kwargs):
    if not instance.pk:
        return
    previous = Reply.objects.filter(pk=instance.pk).first()
    if not previous:
        return
    if previous.status != instance.status and instance.status == ReplyStatus.ACCEPTED:
        send_mail(
            subject='Ваш отклик принят',
            message=f'Ваш отклик на "{instance.post.title}" был принят автором.',
            from_email=None,
            recipient_list=[instance.author.email],
            fail_silently=True
        )
