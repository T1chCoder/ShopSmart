from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import *
from leads.views import *

urlpatterns = [
    #Views
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("cart", CartView.as_view(), name="cart"),
    #Order-Views
    path("orders/active", ActiveOrdersView.as_view(), name="active-orders"),
    path("orders/unpaid", UnpaidOrdersView.as_view(), name="unpaid-orders"),
    path("orders/all", AllOrdersView.as_view(), name="all-orders"),
    #Wishlist-Views
    path("wishlist/products", WishlistProductsView.as_view(), name="wishlist-products"),
    path("wishlist/stores", WishlistStoresView.as_view(), name="wishlist-stores"),
    path("settings", SettingsView.as_view(), name="settings"),
    #Review-Views
    path("reivews/all", AllReviewsView.as_view(), name="all-reviews"),
    path("reivews/mine", MyReviewsView.as_view(), name="my-reviews"),
    path("reivews/liked", LikedReviewsView.as_view(), name="liked-reviews"),
    #Info-Views
    path("address-list", DeliveryAddressesView.as_view(), name="delivery-addresses"),
    path("saved-cards", SavedCardsView.as_view(), name="saved-cards"),
    #Search-Views
    path("search", SearchView.as_view(), name="search"),
    path("search/result", SearchResultView.as_view(), name="search-result"),
    #Registration-Views
    path("sign-up", SignUpView, name="sign-up"),
    path("log-in", LogInView, name="log-in"),
    path("log-out", LogoutView.as_view(), name="log-out"),
    #More-URL
    path("", include("leads.urls.detail"), name="details"),
    path("form/", include("leads.urls.form"), name="forms"),
    path("api/v1", include("leads.urls.api.v1.main"), name="api-v1"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)