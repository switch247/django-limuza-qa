import os
from django.contrib.auth import get_user_model

# Fetch the email and new password from environment variables or set default values
email = os.getenv('USER_EMAIL', 'testuser@test.com')
new_password = os.getenv('USER_NEW_PASSWORD', 'new_password')

User = get_user_model()

try:
    user = User.objects.get(email=email)
    user.set_password(new_password)
    user.save()
    print(f"Password for {email} has been updated.")
except User.DoesNotExist:
    print(f"No user found with the email {email}.")
