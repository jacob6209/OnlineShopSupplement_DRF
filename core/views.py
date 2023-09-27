from http.client import HTTPResponse
from djoser.views import UserViewSet
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from rest_framework.decorators import action
from djoser import signals
from djoser.conf import settings
from djoser.compat import get_user_email

class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
 
        # this line is the only change from the base implementation.
        kwargs['data'] = {"uid": self.kwargs['uid'], "token": self.kwargs['token']}
 
        return serializer_class(*args, **kwargs)

    @action(["get"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.confirmation(self.request, context).send(to)

        # Check if activation was successful
        if user.is_active:
            # Redirect to confirmation.html on success
            # return JsonResponse({'success': True,'massage':'your Registration Was Successfully'})
            return redirect(reverse('confirmation_page'))
            # return JsonResponse({'success': True,'massage':'your Registration Was Successfully'})
        else:
            # Redirect to error.html on failure
           return JsonResponse({'success': False,'massage':'Somthing Went Wrong,please Try Again'})
