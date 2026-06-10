from django.db import models

# Create your models here.

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    consented = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email