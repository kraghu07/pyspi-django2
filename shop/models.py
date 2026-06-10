from django.db import models
from django.utils.text import slugify

class ProductCategory(models.Model):
    product_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_image = models.ImageField(upload_to='category_images/')
    category_description = models.TextField()
    size_category = models.ForeignKey('SizeCategory', on_delete=models.SET_NULL, null=True, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    slug = models.SlugField(unique=True, max_length=255,null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class SizeCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=255)
    brand_description = models.TextField()

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    model_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    model_wearing = models.CharField(max_length=255, null=True, blank=True)
    care_instructions = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255,null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class ProductItem(models.Model):
    product_item_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    colour = models.ForeignKey('Colour', on_delete=models.SET_NULL, null=True, blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name} - {self.colour.colour_name if self.colour else 'No Colour'}"


class ProductImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    image_filename = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image of {self.product_item}"


class ProductVariation(models.Model):
    variation_id = models.AutoField(primary_key=True)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    size = models.ForeignKey('SizeOption', on_delete=models.CASCADE)
    qty_in_stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_item} - {self.size.size_name}"


class SizeOption(models.Model):
    size_id = models.AutoField(primary_key=True)
    size_name = models.CharField(max_length=255)
    sort_order = models.IntegerField(null=True, blank=True)
    size_category = models.ForeignKey(SizeCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.size_name


class Colour(models.Model):
    colour_id = models.AutoField(primary_key=True)
    colour_name = models.CharField(max_length=255)

    def __str__(self):
        return self.colour_name
