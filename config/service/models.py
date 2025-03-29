from django.db import models
# from service_category.models import ServiceCategory
from django.utils import timezone

class ActiveServiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=None)


# Servislar uchun model
class Service(models.Model):
    phone_number = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    managers = models.ManyToManyField("manager.Manager", related_name="services")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()
    active_objects = ActiveServiceManager()

    class Meta:
        verbose_name = "Servis"
        verbose_name_plural = "Servislar"

    def __str__(self):
        return self.title
    

    def safe_delete(self):
        self.is_deleted = timezone.now()
        self.save()
        return True
    

    def restore(self):
        self.is_deleted = None
        self.save()
        return True