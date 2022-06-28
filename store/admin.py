from django.contrib import admin
from .models import Product,ReviewRating
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','Price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}
    list_filter=('category',)




admin.site.register(Product,ProductAdmin)
admin.site.register(ReviewRating)