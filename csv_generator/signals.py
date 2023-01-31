from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GeneratedData
from .tasks import generate_csv_task

@receiver(post_save, sender=GeneratedData)
def generate_csv_file(sender, instance, created, **kwargs):
    if created:
        generate_csv_task.delay(
            instance_id = instance.id,
            )
