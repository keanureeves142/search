from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=50, unique=True)
    product_name = models.TextField()
    category = models.TextField()
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.CharField(max_length=10)  # Stored as string to preserve symbols like '%'
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    rating_count = models.IntegerField()

    def __str__(self):
        return self.product_name


class ProductIndex(models.Model):
    product_id = models.CharField(max_length=50, unique=True, primary_key=True)
    name_tokens = models.TextField()
    categories = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.CharField(max_length=10)  # Stored as string to preserve symbols like '%'
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    rating_count = models.IntegerField()

    def __str__(self):
        return self.product_id
