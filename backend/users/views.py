from django.contrib.auth import get_user_model
from rest_framework import status, views, response
from rest_framework.permissions import AllowAny


class CreateSampleUsers(views.APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        User = get_user_model()

        users_data = [
            ('user1', 'password1'),
            ('user2', 'password2'),
            ('user3', 'password3'),
            ('user4', 'password4'),
            ('user5', 'password5'),
        ]
        
        for username, password in users_data:
            User.objects.create_user(username=username, password=password)

        return response.Response({"message": "Successfully created sample users"}, status=status.HTTP_201_CREATED)
