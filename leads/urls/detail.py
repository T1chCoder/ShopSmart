from django.urls import path
from leads.views import *

app_name = "details"

urlpatterns = [
    path("product/<slug:slug>", ProductDetailView.as_view(), name="product"),
    path("category/<slug:slug>", CategoryDetailView.as_view(), name="category"),
    path("store/<slug:slug>", StoreDetailView.as_view(), name="store"),
    path("profile/<slug:slug>", ProfileDetailView.as_view(), name="profile"),
]