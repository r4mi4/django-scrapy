from django.db import models


class Exchange(models.Model):
    company = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    explanation = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company

