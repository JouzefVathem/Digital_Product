import random, uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.cache import cache

from .models import User, Device

class RegisterView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try :
            user = User.objects.get(phone_number=phone_number)
            return Response({'detail': 'User already registered!'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            code = random.randint(10000, 99999)

            # send message
            # cache 
            cache.set(str(phone_number), code, 2 * 60)

            return Response({'code': code})
        
        # user, created = User.objects.get_or_create(phone_number=phone_number)
        


class GetTokenView(APIView):
    
    def post (self, request):
        
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        cached_code = cache.get(str(phone_number))
        if code != cached_code or cached_code is None:
            return Response({"detail": "Invalid code"}, status=status.HTTP_403_FORBIDDEN)
        else:
            user = User.objects.create_user(phone_number=phone_number)
            token = str(uuid.uuid4())
            device = Device.objects.create(user=user)
            return Response({'token': token})