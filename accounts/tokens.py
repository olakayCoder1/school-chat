import secrets
from django.contrib.auth import get_user_model
from .models import TokenActivation




def account_activation_token():
    return secrets.token_hex(32)

User = get_user_model()



def check_token(user, token):
    check_token = TokenActivation.objects.filter(user_id=user,token=token)
    print(check_token)
    if check_token.count() > 0 :
        check_token.delete()
        return True
    else:
        return False
