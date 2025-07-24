from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Action, Follow, Task

User = get_user_model()


@receiver(post_save, sender=Task)
def create_task_action(sender, instance, created, **kwargs):
    action_type = 'task_create' if created else 'task_update'
    Action.objects.create(
        profile=instance.author,
        action=action_type,
        description=f'Задача "{instance.title}" была создана.'
    )


@receiver(pre_delete, sender=Task)
def delete_task_action(sender, instance, **kwargs):
    Action.objects.create(
        profile=instance.author,
        action='task_delete',
        description=f'Задача "{instance.title}" была удалена.'
    )


@receiver(post_save, sender=User)
def user_action(sender, instance, created, **kwargs):
    action_type = 'create' if created else 'update'
    Action.objects.create(
        profile=instance,
        action=action_type,
        description=f'Пользователь {instance.username} был '
                    f'{"создан" if created else "обновлен"}.'
    )


@receiver(post_save, sender=Follow)
def follow_action(sender, instance, created, **kwargs):
    if created:
        Action.objects.create(
            profile=instance.user,
            action='follow',
            description=f'Пользователь {instance.user.username} подписался на '
                        f'{instance.following.username}'
        )


@receiver(pre_delete, sender=Follow)
def unfollow_action(sender, instance, **kwargs):
    Action.objects.create(
        profile=instance.user,
        action='unfollow',
        description=f'Пользователь {instance.user.username} отписался от '
                    f'{instance.following.username}'
    )
