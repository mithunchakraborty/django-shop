from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Product category
    """
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'category'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:get_product_list_view_by_category',
            args=[self.slug]
        )


class Product(models.Model):
    """
    Store goods
    """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)

    # Alias of product (This URL)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) 

    # Balance of goods
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'), )
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'product'

    def __str(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:get_product_detail_view',
            args=[self.id, self.slug]
        )

