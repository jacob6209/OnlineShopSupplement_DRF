from django.dispatch import receiver
from store.signals import order_created

@receiver(order_created)
def After_Payment_was_Successfull(sender,instance,**kwargs):
    order = instance
    print(f'New Payment Was Successfull!Order Number is:{order.id}')