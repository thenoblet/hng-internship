import pytest
from django.conf import settings
from users.models import User, Organisation


@pytest.mark.django_db
def test_organisation_access_control():
    # Create users
    user1 = User.objects.create_user(email='user1@example.com', password='password1', username='user1')
    user2 = User.objects.create_user(email='user2@example.com', password='password2', username='user2')
    
    # Create organisations
    org1 = Organisation.objects.create(name="Org1", description="First organisation")
    org2 = Organisation.objects.create(name="Org2", description="Second organisation")
    
    # Associate users with organisations
    org1.users.add(user1)
    org2.users.add(user2)
    
    # User 1 should have access to org1 but not org2
    assert org1 in user1.organisations.all()
    assert org2 not in user1.organisations.all()
    
    # User 2 should have access to org2 but not org1
    assert org2 in user2.organisations.all()
    assert org1 not in user2.organisations.all()
