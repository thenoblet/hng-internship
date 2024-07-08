import pytest
from django.urls import reverse
from django.test import Client
from users.models import User, Organisation
from rest_framework.test import APIClient
from rest_framework import status

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_successful_registration(client):
    url = reverse('user_registration')
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'securepassword'
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert 'accessToken' in response.data['data']
    print(response.data)
    assert 'user' in response.data['data']
    assert response.data['data']['user']['email'] == 'john.doe@example.com'
    


@pytest.mark.django_db
def test_register_user_with_default_organisation():
    client = APIClient()
    url = reverse('user_registration')
    data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "1234567890"
    }
    
    response = client.post(url, data, format='json')
    print(response.data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'accessToken' in response.data['data']
    assert response.data['data']['user']['firstName'] == 'John'
    
    user = User.objects.get(email='john.doe@example.com')
    organisation = Organisation.objects.filter(users=user).first()
    
    assert organisation.name == "John's Organisation"


@pytest.mark.django_db
def test_missing_required_fields(client):
    url = reverse('user_registration')
    data = {
        'firstName': '',
        'lastName': '',
        'email': '',
        'password': ''
    }
    response = client.post(url, data)
    assert response.status_code == 400
    assert response.data['statusCode'] == 400 
    
    
@pytest.mark.django_db
def test_duplicate_email(client):
    # Create a user with the same email first
    User.objects.create_user(
        email='test@example.com',
        password='password123',
        username='testuser1',
        first_name='Jane',
        last_name='Smith'
    )
    
    url = reverse('user_registration')
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'test@example.com',
        'password': 'securepassword'
    }
    response = client.post(url, data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_user():
    client = APIClient(enforce_csrf_checks=False)
    
    # Create a user first
    user = User.objects.create_user(
        email='john.doe@example.com',
        password='password123',
        firstName='John',
        lastName='Doe',
        username='johndoe'  # Assuming username is required
    )
    
    # Ensure the user is active
    user.is_active = True
    user.save()
    
    url = reverse('user_login')
    
    data = {
        "email": "john.doe@example.com",
        "password": "password123"
    }
    
    response = client.post(url, data, format='json')
    
    print(response.data)
    
    assert response.status_code == status.HTTP_200_OK
    assert 'accessToken' in response.data['data']
    assert response.data['data']['user']['firstName'] == 'John'
