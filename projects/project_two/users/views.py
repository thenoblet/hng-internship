from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, OrganisationSerializer
from .models import User, Organisation
from .utils import generate_refresh_token, generate_token, JWTAuthentication


class UserRegistration(APIView):
    """
    API view for user registration.

    This view handles the registration of a new user. It validates the user data,
    creates a new user, creates a default organisation for the user, and generates
    authentication tokens for the user.

    Attributes:
        permission_classes (tuple): Specifies the permission classes for the view.
    """
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            org = Organisation.objects.create(name=f"{user.firstName}'s Organisation")
            org.users.add(user)
            access_token = generate_token(user)
            refresh_token = generate_refresh_token(user)
            return Response({
                "status": "success",
                "message": "Registration Successful",
                "data": {
                    "access_token": access_token,
                    "user": serializer.data
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400
        }, status=status.HTTP_400_BAD_REQUEST)

        
        
class UserLogin(APIView):
    """
    API view for user login.

    This view handles the login process for users. It verifies the user's email
    and password, generates authentication tokens, and returns the user data 
    and tokens upon successful authentication.

    Attributes:
        permission_classes (tuple): Specifies the permission classes for the view.

    Methods:
        post(request):
            Handle POST request for user login. Verifies user credentials, 
            generates tokens, and returns user data and tokens in the response.
    """
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")
        
        if user.is_active:
            access_token = generate_token(user)
            refresh_token = generate_refresh_token(user)
            
            user_serializer = UserSerializer(user)
            
            response = Response()
            response.set_cookie(key='access-token', value=access_token, httponly=True)
            response.data = {
				"status": "success",
				"message": "Login successfull",
				"data": {
					"accessToken": access_token,
					"user": user_serializer.data
				}
			}
            response.status_code = status.HTTP_200_OK
            return response
        
        return Response({
			"status": "Bad request",
			"message": "Authentication Failed",
			"statusCode": 401
		}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class UserDetail(APIView):
    """
    API view for retrieving user details.

    This view handles the retrieval of user details for a specified user ID.
    It requires authentication and returns the user data upon successful 
    retrieval.

    Attributes:
        authentication_classes (tuple): Specifies the authentication classes for the view.

    Methods:
        get(request, user_id):
            Handle GET request to retrieve user details. Retrieves the user data 
            for the specified user ID and returns it in the response.
    """
    authentication_classes = (JWTAuthentication,)
    
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user)
        return Response({
			"status": "success",
			"message": "User data retrieved successfully",
			"data": serializer.data
		}, status=status.HTTP_200_OK)

     
class OrganisationList(APIView):
    """
    API view for retrieving organisations associated with the authenticated user.

    This view retrieves a list of organisations that the authenticated user is 
    associated with. Requires JWT authentication and returns the organisations' 
    data upon successful retrieval.

    Attributes:
        authentication_classes (tuple): Specifies the authentication classes for the view.
        permission_classes (tuple): Specifies the permission classes for the view.

    Methods:
        get(request):
            Handle GET request to retrieve organisations associated with the authenticated user.
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        organisations = request.user.organisations.all()
        serializer = OrganisationSerializer(organisations, many=True)
        
        response = Response()
        response.data = {
			"status": "success",
			"message": "Organisations Retrieved Successfully",
			"data": {
				"organisations": serializer.data
			}
		}
        response.status_code = status.HTTP_200_OK
        return response

    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            organisation.users.add(request.user)
            return Response({
				"status": "success",
				"message": "Organisation created successfully",
				"data": serializer.data
			}, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
		}, status=status.HTTP_400_BAD_REQUEST)


class OrganisationDetail(APIView):
    """
    API view for retrieving details of a specific organisation.

    This view retrieves details of a specific organisation identified by its ID 
    (`org_id`). Requires JWT authentication and permission to access details of 
    organisations associated with the authenticated user.

    Attributes:
        authentication_classes (tuple): Specifies the authentication classes for the view.
        permission_classes (tuple): Specifies the permission classes for the view.

    Methods:
        get(request, org_id):
            Handle GET request to retrieve details of a specific organisation identified 
            by its ID (`org_id`).
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, org_id):
        organisation = Organisation.objects.get(pk=org_id)
        if request.user in organisation.users.all():
            serializer = OrganisationSerializer(organisation)
            return Response({
				"status": "success",
				"message": "Organisation retrieved successfully",
				"data": serializer.data
			}, status=status.HTTP_200_OK)
        
        return Response({
			"status": "Bad request",
			"message": "Access denied"
		}, status=status.HTTP_403_FORBIDDEN)


class AddUserToOrganisation(APIView):
    """
    API view for adding a user to an organisation.

    This view allows adding a user identified by their ID (`userId`) to an organisation 
    identified by its ID (`org_id`). Requires JWT authentication and permission to modify 
    organisations associated with the authenticated user.

    Attributes:
        authentication_classes (tuple): Specifies the authentication classes for the view.
        permission_classes (tuple): Specifies the permission classes for the view.

    Methods:
        post(request, org_id):
            Handle POST request to add a user to an organisation identified by its ID 
            (`org_id`).
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, org_id):
        try:
            organisation = get_object_or_404(Organisation, pk=org_id)
        except Organisation.DoesNotExist:
            return Response({
				"status": "Error",
				"message": f"Organisation with id {org_id} does not exist"
			}, status=status.HTTP_404_NOT_FOUND)
        
        user_id = request.data.get('userId')
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({
				"status": "Error",
				"message": f"User with id {user_id} does not exist"
			}, status=status.HTTP_404_NOT_FOUND)
            
        organisation.users.add(user)
            
        return Response({
			"status": "success",
			"message": "User added to organisation successfully"
		}, status=status.HTTP_200_OK)
