from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Due to the nature of path - the order here matters
urlpatterns = [
    # Vessels api
    path('', views.getRoutes),
    path('vessels/', views.retrieveUserVessels, name='retrieve-user-vessels'),
    path('vessels/all', views.retrieveVessels, name='retrieve-all-vessels'),
    path('vessels/add', views.addVessel, name='add-vessel'),
    path('vessels/<str:id>', views.retrieveUserVessel, name='retrieve-vessel'),
    path('vessels/update/<str:id>', views.updateVessel, name='update-vessel'),
    path('vessels/remove/<str:id>', views.deleteVessel, name='remove-vessel'),

    # User token path
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
]
