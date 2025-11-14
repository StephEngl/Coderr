import os
from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete


def overwrite_file_upload(instance, filename):
    """
    Custom upload_to function that deletes old file when uploading new one.
    Usage: image = models.ImageField(upload_to=overwrite_file_upload)
    """
    # Get the model name and instance pk for unique path
    model_name = instance.__class__.__name__.lower()
    
    # Create directory structure
    upload_path = f"{model_name}s/{instance.pk or 'temp'}"
    
    # If instance has pk (existing object), delete old file
    if instance.pk:
        try:
            old_instance = instance.__class__.objects.get(pk=instance.pk)
            # Check if the field that's being updated has a file
            for field in instance._meta.fields:
                if hasattr(field, 'upload_to') and hasattr(old_instance, field.name):
                    old_file = getattr(old_instance, field.name)
                    if old_file and default_storage.exists(old_file.name):
                        default_storage.delete(old_file.name)
        except instance.__class__.DoesNotExist:
            pass
    
    return f"{upload_path}/{filename}"


@receiver(post_delete)
def delete_file_on_delete(sender, instance, **kwargs):
    """
    Signal to delete file when model instance is deleted.
    """
    for field in instance._meta.fields:
        if hasattr(field, 'upload_to'):
            file_field = getattr(instance, field.name)
            if file_field and default_storage.exists(file_field.name):
                default_storage.delete(file_field.name)