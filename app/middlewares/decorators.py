from functools import wraps
import jwt
from django.conf import settings
from rest_framework.response import Response
from app.models import Client
from app.constants.messageConstants import *

def require_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        try:
            decoded_data = jwt.decode(jwt=auth_header, key=settings.SECRET_KEY,algorithms=["HS256"])
            client_id = decoded_data['user_id'] 
            client_details = Client.objects.filter(id=decoded_data['user_id']).values()
            return view_func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return Response({'success': False, 'message': TOKEN_EXPIRED}, status=401)
        except jwt.DecodeError:
            return Response({'success': False, 'message': TOKEN_REQUIRE}, status=422)     
    return _wrapped_view