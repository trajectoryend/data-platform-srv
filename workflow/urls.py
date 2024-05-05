from django.urls import include, re_path
from rest_framework.routers import SimpleRouter


router = SimpleRouter(False)


urlpatterns = [
    re_path('', include(router.urls))
]
