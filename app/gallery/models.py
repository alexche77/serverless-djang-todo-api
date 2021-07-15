from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.image.name}'

    class Meta:
        verbose_name_plural = 'Images'
