from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from .models import Task


@receiver(post_save, sender=Task)
def clear_task_cache_on_create(sender, instance, created, **kwargs):
    if not created:
        return

    charity_user_id = instance.charity.user.id

    # حذف تمام کش‌های مربوط به تسک‌های این کاربر
    print("signal called")
    cache.delete_pattern(f"tasks:user:{charity_user_id}:*")
