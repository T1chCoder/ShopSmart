from django.urls import path
from leads.views import *

app_name = "forms"

urlpatterns = [
    path("cart/add", AddToCartFormView, name="add-to-cart"),
    path("review/send", SendReviewFormView, name="send-review"),
    #Favorite
    path("wishlist/add", LikeProductFormView, name="like-product"),
    path("store/subscribe", SubscribeStoreFormView, name="subscribe-store"),
    path("review/like", LikeReviewFormView, name="like-review"),
    #Cart
    path("cart/product/remove", RemoveFromCartFormView, name="remove-from-cart"),
    path("cart/product/quantity/change", ChangeCartQuantityFormView, name="change-cart-quantity"),
    path("cart/product/select", SelectCartFormView, name="select-cart"),
]