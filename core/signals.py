from django.dispatch import receiver
from store.signals import order_created
from pyfcm import FCMNotification

@receiver(order_created)
def After_Payment_was_Successfull(sender,instance,**kwargs):
    order = instance
    # Replace 'YOUR_FCM_SERVER_KEY' with your actual FCM server key
    api_key = 'AAAAOVG4xeE:APA91bEIkg7uVx4uE8FxmM64ZbaLisaSGeWVXmBq9TtMiFlM-jY0UMs9P0MG0nst7UCW9rHCeEyLwG2LwcARlfEZx7_tZ2kkFpPWvIbWU_PXdSUj1zUG3ICcxfsetQCIlI6xFRb2nZUu'

    # Replace 'staff_group' with the actual topic name for your staff group
    topic_name = 'staff_group'

    # Create an instance of FCMNotification with the API key
    push_service = FCMNotification(api_key=api_key)

    # Construct the message with the specific topic
    message = {
    "to": f"/topics/{topic_name}",
    "notification": {
        "title": "You Have New Order!",
        "body": f'New Payment Was Successful! Order Number is: {order.id}'
    },
    "data": {
        "title": "You Have New Order!",
        "body": f'New Payment Was Successful! Order Number is: {order.id}'
    }
    }

    # Send the notification to the specified topic
    result = push_service.notify_topic_subscribers(topic_name=topic_name, data_message=message)
    print(f'Result of push notification: {result}')
    # # Replace 'YOUR_FCM_SERVER_KEY' with your actual FCM server key
    # api_key ='AAAAOVG4xeE:APA91bEIkg7uVx4uE8FxmM64ZbaLisaSGeWVXmBq9TtMiFlM-jY0UMs9P0MG0nst7UCW9rHCeEyLwG2LwcARlfEZx7_tZ2kkFpPWvIbWU_PXdSUj1zUG3ICcxfsetQCIlI6xFRb2nZUu'

    # # Replace 'admin_registration_token' with the actual FCM registration token of the admin's device
    # admin_registration_token ='cLExiQ-fS66wtGXyPnGE4u:APA91bHJoZaq1qxVDm1arSrRrZY3LOnb9ZSq1v58YPbJSEich5Q8OecjkpvofLWJcH2Fuc_byFeR3nu2EScWjpFaJ2t_Ykt7CtgDmidIh1etyDXuhMregx2XUyh0MlUUKa6yDOVPvyAb'

    # # Create an instance of FCMNotification with the API key
    # push_service = FCMNotification(api_key=api_key)

    # # Construct the message with the specific registration token
    # message = {
    #     "registration_ids": [admin_registration_token],
    #     "notification": {
    #         "title": "You Have New Order!",
    #         "body": f'New Payment Was Successfull!Order Number is: {order.id}'
    #     }
    # }

    # # Send the notification
    # result = push_service.notify_single_device(registration_id=admin_registration_token, data_message=message)
    # print(f'Result of push notification: {result}')