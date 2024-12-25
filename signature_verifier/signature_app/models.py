from django.db import models

# Create your models here.

class Signature(models.Model):
    original_image = models.ImageField(upload_to='signatures/originals/')
    test_image = models.ImageField(upload_to='signatures/tests/')
    result = models.CharField(max_length=50, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signature {self.id} - Result: {self.result}"
