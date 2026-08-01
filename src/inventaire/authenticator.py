from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class CardAuthenticateBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        my_user_model = get_user_model()
        try:
            print(username, password)
            user = my_user_model.objects.get(Q(username=username)|Q(cardid=username))
            print(user)
            if user.check_password(password):
                return user # return user on valid credentials
        except my_user_model.DoesNotExist:
            return None # return None if custom user model does not exist
        except:
            return None # return None in case of other exceptions

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None
