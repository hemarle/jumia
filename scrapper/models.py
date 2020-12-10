from django.db import models

# Create your models here.
class Search(models.Model):
    search_text=models.CharField(max_length=500)

    def __str__(self):
        return self.search_text

class Results(models.Model):
    search_text=models.ForeignKey(Search, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=500)
    product_price=models.CharField(max_length=500)
    product_info=models.TextField(max_length=1500)