from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    """Задача."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False, verbose_name='Завершена')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Action(models.Model):
    """Действия пользователя."""
    ACTION_TYPES = (
        ('task_create', 'Создание задачи'),
        ('task_update', 'Обновление задачи'),
        ('task_delete', 'Удаление задачи'),
    )

    profile = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actions',
        verbose_name='Пользователь'
    )
    action = models.CharField(
        'Действие',
        choices=ACTION_TYPES,
        max_length=50
    )
    description = models.TextField('Описание')
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'
        ordering = ('-created_at',)

    def __str__(self):
        return self.action


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Подписки'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_following'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='prevent_self_follow'
            ),
        ]