from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator
from django_countries.fields import CountryField

class UsersModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # Link to User model
    full_name = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.CharField(max_length=255, unique=True, null=False, validators=[EmailValidator()])
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username

    def get_addresses(self):
        return ", ".join([str(address) for address in self.addresses.all()])


class Address(models.Model):
    user = models.ForeignKey(UsersModel, on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=100, null=False)
    apartment_address = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField(null=False)
    pincode = models.CharField(max_length=100, null=False)
    address_type = models.CharField(max_length=100, choices=[('B', 'Billing'), ('S', 'Shipping')], null=False)
    default = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.street_address

class Payment(models.Model):
    user = models.ForeignKey(UsersModel, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return str(self.amount)

class OrderItem(models.Model):
    user = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False, null=False)
    productitem = models.ForeignKey('ProductItem', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=False)
    size = models.ForeignKey('SizeOption', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} of {self.productitem}"


class Order(models.Model):
    user = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, null=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True, null=False)
    ordered_date = models.DateTimeField(null=False)
    ordered = models.BooleanField(default=False, null=False)
    shipping_address = models.ForeignKey(Address, related_name='shipping_orders', on_delete=models.SET_NULL, null=True, blank=True)
    billing_address = models.ForeignKey(Address, related_name='billing_orders', on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    being_delivered = models.BooleanField(default=False, null=False)
    received = models.BooleanField(default=False, null=False)
    refund_requested = models.BooleanField(default=False, null=False)
    refund_granted = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.user.username

class brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.brand_name

class product_category(models.Model):
    product_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    category_description = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to="product_category",blank=True, null=True)
    size_category_id = models.ForeignKey('self', on_delete=models.CASCADE, related_name='size_categories', null=True, blank=True)
    parent_category_id = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subcategories', null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_category = models.ForeignKey(product_category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(brand, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    model_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    model_wearing = models.CharField(max_length=255, null=True, blank=True)
    care_instructions = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product_name

class Colour(models.Model):
    colour_id = models.AutoField(primary_key=True)
    colour_name = models.CharField(max_length=255)

    def __str__(self):
        return self.colour_name


class SizeCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class SizeOption(models.Model):
    size_id = models.AutoField(primary_key=True)
    size_name = models.CharField(max_length=255)
    sort_order = models.IntegerField()
    size_category = models.ForeignKey(SizeCategory, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    qty_in_stock = models.PositiveIntegerField(default=0)  # Add this field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.size_name}-{self.size_category}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.size_name



class ProductItem(models.Model):
    product_item_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE, null=True)
    size_category = models.ForeignKey(SizeCategory, on_delete=models.CASCADE, blank=True, null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_code = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    image1 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    size_options = models.ManyToManyField(SizeOption)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product.product_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.product_name} - {self.colour.colour_name}'

class ProductVariation(models.Model):
    variation_id = models.AutoField(primary_key=True)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    size = models.ForeignKey('SizeOption', on_delete=models.CASCADE)
    qty_in_stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_item} - {self.size.size_name}"

