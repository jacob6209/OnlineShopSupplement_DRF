from django.urls import path

from payment.views import payment_process,payment_callback,payment_process_sandbox,payment_callback_sandbox

app_name='payment'

urlpatterns = [
    # path('process/<int:order_id>',payment_process,name='payment_process'),
    # path('callback/',payment_callback,name='payment_callback'),
    
    path('process/<int:order_id>',payment_process_sandbox,name='payment_process'),
    path('callback/',payment_callback_sandbox,name='payment_callback'),

]