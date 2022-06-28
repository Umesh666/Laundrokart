from django.contrib import admin
from .models import Order,Payment,OrderProduct

class OrderProductInline(admin.TabularInline):
    model=OrderProduct
    readonly_fields=('payment','user','product','quantity','product_price','ordered','category')
    extra=0
class orderAdmin(admin.ModelAdmin):
    list_display=['order_number','full_name','phone','email','city','order_total','tax','status','is_ordered']
    list_filter=['status','is_ordered']
    search_fields=['order_number','first_name','last_name','phone','email']
    list_per_page=30
    inlines=[OrderProductInline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display=['order_id','payment','user','product','category','quantity','product_price','ordered']
    search_fields=['order','user','product']
    list_per_page=30

class PaymentAdmin(admin.ModelAdmin):
    list_display=['payment_id','payment_method','amount_paid','status']
    readonly_fields=('payment_id','payment_method','amount_paid','status')
admin.site.register(Order,orderAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)

# Register your models here.
