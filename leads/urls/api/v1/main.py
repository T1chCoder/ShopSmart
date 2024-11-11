from django.urls import path
from leads.views import *
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r"user", UserAPIView)
router.register(r"store", StoreAPIView)
router.register(r"chat", ChatAPIView)
router.register(r"category", CategoryAPIView)
router.register(r"banner", BannerAPIView)
router.register(r"product", ProductAPIView)
router.register(r"order", OrderAPIView)
router.register(r"review", ReviewAPIView)

app_name = "api"

urlpatterns = [
    path("/", include(router.urls), name="users"),
    path("/", include(router.urls), name="stores"),
    path("/", include(router.urls), name="chats"),
    path("/", include(router.urls), name="categories"),
    path("/", include(router.urls), name="banners"),
    path("/", include(router.urls), name="products"),
    path("/", include(router.urls), name="orders"),
    path("/", include(router.urls), name="reviews"),
]