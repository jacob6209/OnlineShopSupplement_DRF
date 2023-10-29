from rest_framework.response import Response
from django.urls import reverse
import requests,json
from django.shortcuts import render,get_object_or_404,redirect
from orders.models import Order
from django.http import HttpResponse,HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer


# Create your views here.

def  payment_process(request,order_id):
    #Get Order id 
    # order_id=request.data.get('order_id')
    #Get the Order Object
    order=get_object_or_404(Order,id=order_id)

    toman_total_price = order.get_total_price()

    rial_total_price = toman_total_price*10

    ZarinPal_Request_Url='https://api.zarinpal.com/pg/v4/payment/request.json'
    request_header={
        'accept':'application/json',
        'content-type':'application/json'
    }
    request_data = {
        'merchant_id':'aaaabbaaaabbaaaabbaaaabbaaaabbaaaabb',
        'amount':rial_total_price,
        'description':f'#{order.id}:{order.customer.user.first_name} {order.customer.user.last_name}',
        # 'callback_url':'http://127.0.0.1:800'
        'callback_url':request.build_absolute_uri(reverse('payment:payment_callback')),
    }

    print(order.customer.user.first_name)
    print(order.customer.user.last_name)
    res=requests.post(ZarinPal_Request_Url,data=json.dumps(request_data),headers=request_header)
    print(res.json()['data'])
    data=res.json()['data']
    authority=data['authority']
    order.zarinpal_authority=authority
    order.save()
    if 'errors' not in data or len(data['error'])==0 :
        return redirect('https://www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error From ZarinPal')

def payment_callback(request):
    payment_authority=request.Get.get('Authority')
    payment_status=request.GET.get('status')
    
    order=get_object_or_404(order,zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price*10

    if payment_status=='ok':

        request_header={
            'accept':'application/json',
            'content-type':'application/json'
        }
        request_data = {
            'merchant_id':'aaaabbaaaabbaaaabbaaaabbaaaabbaaaabb',
            'amount':rial_total_price,
            'authority':payment_authority
        }

        res=requests.post(
            url='https://api.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header
            )
        
        if 'data' in res.json() and ('errors' not in res.json()['data'] or len (res.json()['data']['errors'])==0):
            data=res.json()['data']
            payment_code=data['code']

            if payment_code==100:
                order.status=order.ORDER_STATUS_PAID
                order.zarinpal_ref_id=data['ref_id']
                order.zarinpal_data=data
                order.save()

                return HttpResponse('Payment Was Successful')
            elif payment_code==101:
                return HttpResponse("Payment Was Successful,However This transaction has already been registered")
            
            else:
                error_code=res.json()['errors']['code']
                error_message=res.json()['errors']['message']
                return HttpResponse(f'transaction was faild, {error_code} {error_message}')

    else:
         return HttpResponse(f'transaction was faild')



    payment_authority=request.Get.get('Authority')
    payment_status=request.GET.get('status')
    
    order=get_object_or_404(order,zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price*10

    if payment_status=='ok':

        request_header={
            'accept':'application/json',
            'content-type':'application/json'
        }
        request_data = {
            'merchant_id':'abcABCabcABCabcABCabcABCabcABCabcABC',
            'amount':rial_total_price,
            'authority':payment_authority
        }

        res=requests.post(
            url='https://api.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header
            )
        
        if 'data' in res.json() and ('errors' not in res.json()['data'] or len (res.json()['data']['errors'])==0):
            data=res.json()['data']
            payment_code=data['code']

            if payment_code==100:
                order.status=order.ORDER_STATUS_PAID
                order.zarinpal_ref_id=data['ref_id']
                order.zarinpal_data=data
                order.save()

                return HttpResponse('Payment Was Successful')
            elif payment_code==101:
                return HttpResponse("Payment Was Successful,However This transaction has already been registered")
            
            else:
                error_code=res.json()['errors']['code']
                error_message=res.json()['errors']['message']
                return HttpResponse(f'transaction was faild, {error_code} {error_message}')

    else:
         return HttpResponse(f'transaction was faild')


@api_view(['GET'])
def  payment_process_sandbox(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    print(order.status)
    print(order.ORDER_STATUS_PAID)
    if  order.status!=order.ORDER_STATUS_PAID:

        print(order.status)

        toman_total_price = order.get_total_price()
        rial_total_price = toman_total_price*10

        ZarinPal_Request_Url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'
        request_header={
            'accept':'application/json',
            'content-type':'application/json'
        }
        rial_total_price_float = float(toman_total_price)
        request_data = {
            'MerchantID':'abcABCabcABCabcABCabcABCabcABCabcABC',
            'Amount':rial_total_price_float,
            'Description':f'#{order.id}:{order.customer.user.first_name} {order.customer.user.last_name}',
            'CallbackURL':request.build_absolute_uri(reverse('payment:payment_callback')),

        }

        res=requests.post(ZarinPal_Request_Url,data=json.dumps(request_data),headers=request_header)
        data=res.json()
        authority=data['Authority']
        order.zarinpal_authority=authority
        order.save()
        if 'errors' not in data or len(data['errors']) == 0:
            return Response({'Success': True,'order_id': order_id,'Linke':f'https://sandbox.zarinpal.com/pg/StartPay/{authority}'})
        else:
            return Response({'Success': False, 'Message': 'Error From ZarinPal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'Success': False, 'Message': 'The payment operation of this order has already been successfully completed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @renderer_classes([JSONRenderer])
def  payment_callback_sandbox(request):
    payment_authority=request.GET.get('Authority')
    payment_status=request.GET.get('Status')
    print(f'payment_authority:{payment_authority},payment_status:{payment_status}')
    order=get_object_or_404(Order,zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price*10

    rial_total_price_float = float(rial_total_price)
    if payment_status=='OK':
        request_header={
            'accept':'application/json',
            'content-type':'application/json'
        }
        request_data = {
            'MerchantID':'abcABCabcABCabcABCabcABCabcABCabcABC',
            'Amount':rial_total_price_float,
            'Authority':payment_authority
        }

        # print(f'payment_status 2:{payment_status}')
        res=requests.post(
            url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json',
            data=json.dumps(request_data),
            headers=request_header
            )
        print(f'res data:{res.json()}')
        if  'errors' not in res.json():
            data=res.json()
            payment_code=data['Status']

            if payment_code==100:
                order.status=order.ORDER_STATUS_PAID
                order.zarinpal_ref_id=data['RefID']
                order.zarinpal_data=data
                order.save()

                # Decrease product inventory
                for  item in order.items.all():
                     item.product.inventory -= item.quantity
                     item.product.soled_item +=item.quantity
                     item.product.save()
         
                return Response({'Success': True, 'Message': 'Payment Was Successful'}, status=status.HTTP_204_NO_CONTENT)
            elif payment_code==101:
                return Response({'Success':True,'Message':'Payment Was Successful,However This transaction has already been registered'},status=status.HTTP_204_NO_CONTENT)
            else:
                error_code=res.json()['errors']['code']
                error_message=res.json()['errors']['message']
                return Response({'Success':False,'Message':f'transaction was faild, {error_code} {error_message}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
         return Response({'Success':False,'Message':'transaction was faild'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         

