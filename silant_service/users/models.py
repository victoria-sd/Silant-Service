from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model


class SilantUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="silant_user_set",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="silant_user_set",
        related_query_name="user",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def get_role(self):
        if self.is_staff:
            return 'manager'
        elif self.groups.filter(name='Клиент').exists():
            return 'client'
        elif self.groups.filter(name='Сервисная организация').exists():
            return 'service_organization'
        else:
            return 'guest'

    def __str__(self):
        return self.username


def create_default_roles(sender, **kwargs):
    groups_to_create = ['Клиент', 'Сервисная организация']
    for group_name in groups_to_create:
        Group.objects.get_or_create(name=group_name)

from django.db.models.signals import post_migrate
post_migrate.connect(create_default_roles, sender=__name__)