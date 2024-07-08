from django.urls import path
from .views import UserRegistration, UserLogin, UserDetail, OrganisationList, OrganisationDetail, AddUserToOrganisation

urlpatterns = [
	path('auth/register', UserRegistration.as_view(), name='user_resgistion'),
	path('auth/login', UserLogin.as_view(), name='user_login'),
	path('api/users/<uuid:user_id>', UserDetail.as_view(), name='get_user'),
	path('api/organisations', OrganisationList.as_view(), name="organisations_list_create"),
	path('api/organisations/<uuid:org_id>', OrganisationDetail.as_view(), name="user_organisation"),
	path('api/organisations/<uuid:org_id>/users', AddUserToOrganisation.as_view(), name="add_user_to_org")
]