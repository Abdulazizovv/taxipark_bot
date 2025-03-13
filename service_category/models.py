from django.db import models


# Servis kategoriyalari uchun model
class ServiceCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kategoriya nomi")
    description = models.TextField(verbose_name="Kategoriya haqida", blank=True, null=True)

    class Meta:
        verbose_name = "Servis kategoriya"
        verbose_name_plural = "Servis kategoriyalari"

    def __str__(self):
        return self.name
