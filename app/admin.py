from django.contrib import admin
from .models import product_category, Product, brand, Colour, ProductItem,SizeCategory,SizeOption,UsersModel, OrderItem, Address, Payment, Order

@admin.register(product_category)
class product_categoryModle(admin.ModelAdmin):
    list_display=['product_category_id','category_name','category_description','category_image','size_category_id','parent_category_id']
@admin.register(Product)
class ProductModle(admin.ModelAdmin):
    list_display=['product_id','product_category','brand','product_name','product_description','model_height','model_wearing','care_instructions','about']
@admin.register(brand)
class brandModle(admin.ModelAdmin):
    list_display=['brand_id','brand_name']
@admin.register(Colour)
class ColourModle(admin.ModelAdmin):
    list_display=['colour_id','colour_name']


@admin.register(ProductItem)
class ProductItemModle(admin.ModelAdmin):
    list_display=['product_item_id','product','colour','original_price','sale_price','product_code','slug','image1','image2','image3','image4']
@admin.register(SizeCategory)
class SizeCategoryModle(admin.ModelAdmin):
    list_display=['category_id','category_name']
@admin.register(SizeOption)
class SizeOptionModle(admin.ModelAdmin):
    list_display=['size_id','size_name','sort_order','size_category']


@admin.register(Payment)
class PaymentModle(admin.ModelAdmin):
    list_display=['user','amount','timestamp']

@admin.register(Address)
class AddressModle(admin.ModelAdmin):
    list_display=['user','street_address','apartment_address','country','pincode','address_type','default']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'productitem', 'quantity', 'size']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ref_code', 'start_date', 'ordered_date', 'ordered', 'being_delivered', 'received']

@admin.register(UsersModel)
class UsersModelAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'full_name', 'username', 'email', 'phone_number', 'profile_picture', 'get_addresses']  # Added get_addresses method

