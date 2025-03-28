from django.db import models
# from service_category.models import ServiceCategory


# Servislar uchun model
class Service(models.Model):
    phone_number = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    managers = models.ManyToManyField("manager.Manager", related_name="services")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Servis"
        verbose_name_plural = "Servislar"

    def __str__(self):
        return self.title