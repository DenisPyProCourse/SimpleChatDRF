from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import ThreadAPIList, MessageApiList, DetailMessageApi, UserAPIList, UserAPIDetail, RegistrUserView

router = routers.SimpleRouter()
router.register(r'threads', ThreadAPIList)

urlpatterns = [
    path('base-auth/', include('rest_framework.urls')),  # Implementation of the basic authentication
    path('register/', RegistrUserView.as_view(), name='register'),  # Standard registration

    path('', include(router.urls)),  # Router for implementation of ViewSet ThreadAPIList (Create,
                                                                                            # Retrieve, List, Delete)
                                            # List/Create: api/v1/threads; Retrieve/Delete: api/v1/threads/pk

    path('threads/<int:pk_thread>/messages/', MessageApiList.as_view()),  # List/Create message for exact thread.
    path('threads/<int:pk_thread>/messages/<int:pk>/', DetailMessageApi.as_view()),  # Message details

    path('users/', UserAPIList.as_view()),  # User list
    path('users/<int:pk>/', UserAPIDetail.as_view()),  # User details

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get the JWT tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh access_token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verify tokens
]
