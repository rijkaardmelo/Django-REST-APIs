from django.urls import path, include
from user.views import UserView, LoginView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('login', LoginView, basename="login")
router.register(r'', UserView, basename="user")


urlpatterns = [
    path('', include(router.urls),)
]
