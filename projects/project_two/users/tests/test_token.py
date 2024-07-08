import pytest
from datetime import datetime, timedelta, timezone
from jwt import decode, encode
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import User
from users.utils import generate_token
from uuid import uuid4

User = get_user_model()

@pytest.mark.django_db
def test_token_expiry():
    user_id = uuid4()
    user = User.objects.create_user(
        userId=user_id,
        email='test@example.com',
        password='password123',
        firstName='John',
        username = 'testuser',
        lastName='Doe'
    )
    
    token = generate_token(user)
    
    decoded_token = decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    
    # Calculate expected expiry time (2 hours from now)
    expected_expiry = datetime.now(timezone.utc) + timedelta(hours=2)
    
    # Ensure token expiry matches expected
    assert decoded_token['exp'] == int(expected_expiry.timestamp())
    assert decoded_token['user_id'] == str(user.userId)
