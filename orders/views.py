from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import OrderForm
import datetime
from .models import Order,Payment,OrderProduct
from carts.models import CartItem
from store.models import Product
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def payments(request):
    body=json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],

    )
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()

    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderProduct=OrderProduct()
        orderProduct.order_id=order.id
        orderProduct.payment=payment
        orderProduct.user_id=request.user.id
        orderProduct.product_id=item.product_id
        orderProduct.quantity=item.quantity
        orderProduct.product_price=item.product.Price
        orderProduct.category=item.product.category
        orderProduct.ordered=True
        orderProduct.save()

        product=Product.objects.get(id=item.product_id)
        product.stock-=item.quantity
        product.save()

    CartItem.objects.filter(user=request.user).delete()

    mail_subject='Thank you for your order!'
    message=render_to_string('orders/order_received_email.html',{
        'user':request.user,
        'order':order,
    })
    to_email=order.email
    send_email=EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()

    data={
        'order_number':order.order_number,
        'transID':payment.payment_id,
    }

    return JsonResponse(data)


def place_order(request,total=0,quantity=0,):
    grand_total=0
    tax=0
    cart_items=CartItem.objects.filter(user=request.user)
    for cart_item in cart_items:
        total+=(cart_item.product.Price*cart_item.quantity)
        quantity+=cart_item.quantity
    tax=(2*total)/100
    grand_total=tax+total
    if request.method=='POST':
        form=OrderForm(request.POST)

        if form.is_valid():
            data=Order()
            data.user=request.user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date+str(data.id)
            data.order_number=order_number
            data.save()

            order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total
            }
            return render(request,'orders/payments.html',context)
        else:
            return redirect('checkout')

def order_complete(request):
    order_number=request.GET.get('order_number')
    transID=request.GET.get('payment_id')

    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products=OrderProduct.objects.filter(order_id=order.id)
        subtotal=0
        for i in ordered_products:
            subtotal+=i.product_price*i.quantity
        payment=Payment.objects.get(payment_id=transID)
        context={
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
        }
        return render(request,'orders/order_complete.html',context)

    except(Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')
