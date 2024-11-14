from django.shortcuts import render
from django.views.generic import *
from django.shortcuts import *
from .models import *
from .forms import *
from .serializers import *
from django.urls import *
from django.contrib.auth.views import *
from django.views.generic.detail import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import viewsets
from django.db.models import Q
from django.db.models import Avg
from django.contrib.auth import authenticate, login
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

email_validator = EmailValidator()

class DefaultView(View):
    page = None
    user_profile = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.page
        if page:
            context[page] = True
            context["page"] = page
        context["website_name"] = settings.WEBSITE_NAME
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            context["user_profile"] = user_profile 
            self.user_profile = user_profile
            context["cart_products_id"] = UserProfileCart.objects.filter(user_profile=user_profile).values_list("product__id", flat=True)
        else:
            context["cart_products_id"] = []
        context["wihslist_products"] = UserProfileFavorite.objects.filter(user_profile=self.user_profile, product__isnull=False).values_list("product__id", flat=True)

        return context
    
class HomeView(DefaultView, ListView):
    model = Product
    context_object_name = "recommended_products"
    template_name = "leads/home.html"
    page = "home_page"
    products = Product.objects.all().filter(is_active=True)
    hot_products = products.filter(is_hot=True)[:9]
    hot_product_ids = hot_products.values_list('id', flat=True)
    popular_products = products.filter(is_popular=True).exclude(id__in=hot_product_ids)[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["banners"] = Banner.objects.all()
        context["hot_products"] = self.hot_products
        context["popular_products"] = self.popular_products

        return context
    
    def get_queryset(self):
        hot_product_ids = self.hot_products.values_list('id', flat=True)
        popular_product_ids = self.popular_products.values_list('id', flat=True)
        
        return self.products.exclude(id__in=hot_product_ids).exclude(id__in=popular_product_ids)
    
class CartView(DefaultView, ListView):
    model = UserProfileCart
    context_object_name = "cart_products"
    template_name = "leads/cart.html"
    page = "cart_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all().filter(is_active=True)
        cart_products = UserProfileCart.objects.filter(user_profile=self.user_profile)
        context["recommended_products"] = products.exclude(id__in=cart_products.values_list("product__id", flat=True))
        products_selected = []
        total_sum = Decimal(0.00)
        for cart in cart_products:
            total_sum += cart.product.price * cart.quantity
            if cart.is_selected:
                products_selected.append(1)
            else:
                products_selected.append(0)
        if 0 in products_selected:
            context["all_selected"] = False 
        else:
            context["all_selected"] = True
        context["cart_products_selected"] = cart_products.filter(is_selected=True)
        context["deliver_price"] = 200.99
        context["total_sum"] = total_sum

        return context
    
    def get_queryset(self):
        user_profile = getattr(self.request.user, 'user_profile', None)
        if user_profile:
            return UserProfileCart.objects.filter(user_profile=user_profile)
        return UserProfileCart.objects.none()

class ActiveOrdersView(DefaultView, ListView):
    model = Order
    context_object_name = "active_orders"
    template_name = "leads/orders/active.html"
    page = "active_orders_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(customer=self.request.user, is_cancelled=False)
        return Order.objects.none()

class UnpaidOrdersView(DefaultView, ListView):
    model = Order
    context_object_name = "unpaid_orders"
    template_name = "leads/orders/unpaid.html"
    page = "unpaid_orders_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(customer=self.request.user, is_cancelled=False, is_paid=False)
        return Order.objects.none()

class AllOrdersView(DefaultView, ListView):
    model = Order
    context_object_name = "orders"
    template_name = "leads/orders/all.html"
    page = "all_orders_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(customer=self.request.user)
        return Order.objects.none()

class WishlistProductsView(DefaultView, ListView):
    model = UserProfileFavorite
    context_object_name = "favorite_products"
    template_name = "leads/wishlist/products.html"
    page = "wishlist_products_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            return UserProfileFavorite.objects.filter(user_profile=user_profile, product__isnull=False)
        return UserProfileFavorite.objects.none()

class WishlistStoresView(DefaultView, ListView):
    model = UserProfileFavorite
    context_object_name = "favorite_stores"
    template_name = "leads/wishlist/stores.html"
    page = "wishlist_stores_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["subscribed_stores_id"] = UserProfileFavorite.objects.filter(user_profile=self.user_profile, store__isnull=False).values_list("store__id", flat=True)

        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            return UserProfileFavorite.objects.filter(user_profile=user_profile, store__isnull=False)
        return UserProfileFavorite.objects.none()

class SettingsView(DefaultView, TemplateView):
    template_name = "leads/settings.html"
    page = "settings_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class AllReviewsView(DefaultView, ListView):
    model = Review
    context_object_name = "reviews"
    template_name = "leads/reviews/all.html"
    page = "all_reviews_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            my_reviews = Review.objects.filter(sender=self.request.user).values_list("id", flat=True)
            liked_reviews = UserProfileFavorite.objects.filter(user_profile=user_profile, review__isnull=False).values_list("review__id", flat=True)
            review_ids = list(my_reviews) + list(liked_reviews)
            return Review.objects.filter(id__in=review_ids)
        return Review.objects.none()
    
class MyReviewsView(DefaultView, ListView):
    model = Review
    context_object_name = "own_reviews"
    template_name = "leads/reviews/mine.html"
    page = "my_reviews_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Review.objects.filter(sender=self.request.user)
        return Review.objects.none()

class LikedReviewsView(DefaultView, ListView):
    model = Review
    context_object_name = "liked_reviews"
    template_name = "leads/reviews/liked.html"
    page = "liked_reviews_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            liked_reviews = UserProfileFavorite.objects.filter(user_profile=user_profile, review__isnull=False).values_list("review__id", flat=True)
            return Review.objects.filter(id__in=liked_reviews)
        return Review.objects.none()

class DeliveryAddressesView(DefaultView, ListView):
    model = UserProfileDeliveryAddress
    context_object_name = "delivery_addresses"
    template_name = "leads/delivery-addresses.html"
    page = "delivery_addresses_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserProfileDeliveryAddress.objects.filter(user_profile=self.user_profile)
        return UserProfileDeliveryAddress.objects.none()

class SavedCardsView(DefaultView, ListView):
    model = UserProfileSavedCard
    context_object_name = "saved_cards"
    template_name = "leads/saved-cards.html"
    page = "saved_cards_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserProfileSavedCard.objects.filter(user_profile=self.user_profile)
        return UserProfileSavedCard.objects.none()

class SearchView(DefaultView, TemplateView):
    template_name = "leads/search/index.html"
    page = "search_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class SearchResultView(DefaultView, ListView):
    model = Product
    context_object_name = "searched_products"
    template_name = "leads/search/result.html"
    page = "search_result_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

#Detail-Views
class ProfileDetailView(DefaultView, DetailView):
    model = User
    slug_field = "id"
    context_object_name = "user_detail"
    template_name = "details/profile.html"
    page = "user_detail_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            seen_products = UserProfileHistory.objects.filter(user_profile=self.user_profile, product__isnull=False, product__is_active=True).order_by("-created")
            products = Product.objects.filter(is_active=True)
            context["seen_products"] = seen_products
            context["recommended_products"] = products.exclude(id__in=seen_products.values_list("product__id", flat=True))

        return context
    
class ProductDetailView(DefaultView, DetailView):
    model = Product
    slug_field = "id"
    context_object_name = "product_detail"
    template_name = "details/product/index.html"
    page = "product_detail_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            UserProfileHistory.objects.filter(user_profile=self.user_profile, product=self.object).delete()
            history = UserProfileHistory(user_profile=self.user_profile, product=self.object)
            history.save()
            wishlist =  UserProfileFavorite.objects.all().filter(user_profile=self.user_profile, product=self.object).first()
            if wishlist:
                context["is_liked"] = True
            else:
                context["is_liked"] = False
            context["user_profile_wishlist_reviews"] = UserProfileFavorite.objects.all().filter(user_profile=self.user_profile).exclude(review__isnull=True).values_list('review', flat=True)

        context["cart_product"] = UserProfileCart.objects.filter(user_profile=self.user_profile, product=self.object).first()
        products = Product.objects.all().filter(is_active=True)
        context["recommended_products"] = products.exclude(id=self.object.id)
        context["current_date"] = datetime.now().date()
        reviews = Review.objects.filter(product=self.object, is_active=True)
        context["reviews"] = reviews
        reviews_rating = reviews.values_list("rating", flat=True)
        average_rating = reviews_rating.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            rounded_rating = round(average_rating * 2) / 2
        else:
            rounded_rating = 0
        context["rating"] = rounded_rating

        for i in range(1, 5+1):
            reviews_count = reviews.count()
            filtered_reviews_count = reviews.filter(rating=i).count()
            if reviews_count > 0:
                context[f"rating_{i}"] = f"{filtered_reviews_count * 100 / reviews_count}%"
            else:
                context[f"rating_{i}"] = 0
        
        delivered_orders_id = Order.objects.filter(is_paid=True, is_cancelled=False, is_delivered=True).values_list("id", flat=True)
        context["sold"] = OrderProduct.objects.filter(order__id__in=delivered_orders_id, product=self.object).count()
        
        reviews_store_rating = Review.objects.filter(product__store=self.object.store, is_active=True).values_list("rating", flat=True)
        average_store_rating = reviews_store_rating.aggregate(Avg('rating'))['rating__avg']
        
        if average_store_rating is not None:
            average_store_rating = min(max(average_store_rating, 0), 5)
            average_store_rating *= 20
            rounded_store_rating = round(average_store_rating, 1)
            if rounded_store_rating.is_integer():
                rounded_store_rating = int(rounded_store_rating)
        else:
            rounded_store_rating = 0
        context["store_rating"] = rounded_store_rating

        return context

class ProductReviewsDetailView(DefaultView, DetailView):
    model = Product
    slug_field = "id"
    context_object_name = "product_detail"
    template_name = "details/product/reviews.html"
    page = "product_reviews_detail_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product=self.object)

        if self.request.user.is_authenticated:
            UserProfileHistory.objects.filter(user_profile=self.user_profile, product=self.object).delete()
            history = UserProfileHistory(user_profile=self.user_profile, product=self.object)
            history.save()
            wishlist =  UserProfileFavorite.objects.all().filter(user_profile=self.user_profile, product=self.object).first()
            if wishlist:
                context["is_liked"] = True
            else:
                context["is_liked"] = False
            context["user_profile_wishlist_reviews"] = UserProfileFavorite.objects.all().filter(user_profile=self.user_profile).exclude(review__isnull=True).values_list('review', flat=True)

        context["cart_product"] = UserProfileCart.objects.filter(user_profile=self.user_profile, product=self.object).first()
        products = Product.objects.all().filter(is_active=True)
        context["recommended_products"] = products.exclude(id=self.object.id)
        context["current_date"] = datetime.now().date()
        reviews = Review.objects.filter(product=self.object, is_active=True)
        context["reviews"] = reviews
        reviews_rating = reviews.values_list("rating", flat=True)
        average_rating = reviews_rating.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            rounded_rating = round(average_rating * 2) / 2
        else:
            rounded_rating = 0
        context["rating"] = rounded_rating

        for i in range(1, 5+1):
            reviews_count = reviews.count()
            filtered_reviews_count = reviews.filter(rating=i).count()
            context[f"rating_{i}"] = f"{filtered_reviews_count * 100 / reviews_count}%"
        
        delivered_orders_id = Order.objects.filter(is_paid=True, is_cancelled=False, is_delivered=True).values_list("id", flat=True)
        context["sold"] = OrderProduct.objects.filter(order__id__in=delivered_orders_id, product=self.object).count()
        
        reviews_store_rating = Review.objects.filter(product__store=self.object.store, is_active=True).values_list("rating", flat=True)
        average_store_rating = reviews_store_rating.aggregate(Avg('rating'))['rating__avg']
        
        if average_store_rating is not None:
            average_store_rating = min(max(average_store_rating, 0), 5)
            average_store_rating *= 20
            rounded_store_rating = round(average_store_rating, 1)
            if rounded_store_rating.is_integer():
                rounded_store_rating = int(rounded_store_rating)
        else:
            rounded_store_rating = 0
        context["store_rating"] = rounded_store_rating
        
        return context

class CategoryDetailView(DefaultView, DetailView):
    model = Category
    slug_field = "id"
    context_object_name = "category_detail"
    template_name = "details/category.html"
    page = "category_detail_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            UserProfileHistory.objects.filter(user_profile=self.user_profile, category=self.object).delete()
            history = UserProfileHistory(user_profile=self.user_profile, category=self.object)
            history.save()
        context["products"] = Product.objects.all().filter(category=self.object)

        return context
    
class StoreDetailView(DefaultView, DetailView):
    model = Store
    slug_field = "id"
    context_object_name = "store_detail"
    template_name = "details/store.html"
    page = "store_detail_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            UserProfileHistory.objects.filter(user_profile=self.user_profile, store=self.object).delete()
            history = UserProfileHistory(user_profile=self.user_profile, store=self.object)
            history.save()
            context["is_subscribed"] = UserProfileFavorite.objects.filter(user_profile=self.user_profile, store=self.object).exists()

        store_products = Product.objects.filter(store=self.object)
        context["store_orders_count"] = OrderProduct.objects.filter(order__is_pending=True, order__is_shifted=True, order__is_paid=True, order__is_delivered=True, order__is_cancelled=False, product__id__in=store_products.values_list("id", flat=True)).count()
        average_rating = Review.objects.filter(product__id__in=store_products.values_list("id", flat=True)).aggregate(Avg("rating"))["rating__avg"]
        if average_rating is not None:
            context["rating"] = round(average_rating * 2) / 2
        else:
            context["rating"] = 0
        return context

#Registration-Views
def SignUpView(request):
    if not request.user.is_authenticated:
        page_1 = "registration_page"
        page_2 = "sign_up_page"
        data = {
            page_1: True,
            page_2: True,
            "page": page_1,
            "page_2": page_2,
        }
        return render(request, "registration/sign-up.html", data)
    else:
        return redirect("home")

def LogInView(request):
    if not request.user.is_authenticated:
        page_1 = "registration_page"
        page_2 = "log_in_page"
        data = {
            page_1: True,
            page_2: True,
            "page": page_1,
            "page_2": page_2,
        }
        return render(request, "registration/log-in.html", data)
    else:
        return redirect("home")

#API-Views
class UserAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StoreAPIView(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class ChatAPIView(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BannerAPIView(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

class ProductAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderAPIView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ReviewAPIView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

#Form-Views
def RemoveFromCartFormView(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        sender_id = data.get("sender_id")
        cart_id = data.get("cart_id")

        user = get_object_or_404(User, id=sender_id)
        user_profile = get_object_or_404(UserProfile, user=user)
        cart = get_object_or_404(UserProfileCart, id=cart_id, user_profile=user_profile)
        total = Decimal(0.00)

        cart.delete()

        cart_products_selected_posters = []

        carts_selected = 0

        for user_profile_cart in UserProfileCart.objects.filter(user_profile=user_profile):
            if user_profile_cart.is_selected:
                carts_selected += 1
                cart_products_selected_posters.append(user_profile_cart.product.product_poster.first().photo.url)
                total += user_profile_cart.product.price * user_profile_cart.quantity

        data = {
            "success": True,
            "message": "Removed from cart successfully",
            "carts_selected": carts_selected,
            "cart_products_selected_posters": cart_products_selected_posters, 
            "total": total
        }
        return JsonResponse(data, safe=False)
    return redirect("home")

def ChangeCartQuantityFormView(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        sender_id = data.get("sender_id")
        cart_id = data.get("cart_id")
        is_plus = data.get("is_plus")

        user = get_object_or_404(User, id=sender_id)
        user_profile = get_object_or_404(UserProfile, user=user)
        cart = get_object_or_404(UserProfileCart, id=cart_id, user_profile=user_profile)

        is_min = False 
        is_max = False
        is_deleted = False 
        cart_products_selected_posters = []
        total = Decimal(0.00)
        sum = Decimal(0.00)
        act_sum = Decimal(0.00)
        carts_selected = 0
        
        if is_plus == True:
            if cart.quantity < cart.product.stock:
                cart.quantity += 1
                cart.save()
        elif is_plus == False:
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
            elif cart.quantity == 1:
                cart.delete()
                is_deleted = True
        
        if cart.quantity == cart.product.stock:
            is_max = True

        if cart.quantity == 1:
            is_min = True

        for user_profile_cart in UserProfileCart.objects.filter(user_profile=user_profile):
            if user_profile_cart.is_selected:
                carts_selected += 1
                cart_products_selected_posters.append(user_profile_cart.product.product_poster.first().photo.url)
                total += user_profile_cart.product.price * user_profile_cart.quantity

        sum = cart.quantity * cart.product.price
        act_sum = cart.quantity * cart.product.act_price

        data = {
            "success": True,
            "message": "Cart quantity successfully changed",
            "quantity": cart.quantity,
            "is_min": is_min,
            "is_max": is_max,
            "is_deleted": is_deleted,
            "cart_products_selected_posters": cart_products_selected_posters,
            "carts_selected": carts_selected, 
            "total": total,
            "sum": sum,
            "act_sum": act_sum,
        }
        return JsonResponse(data, safe=False)
    return redirect("home")

def SelectCartFormView(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        sender_id = data.get("sender_id")
        cart_id = data.get("cart_id")
        all = data.get("all")

        user = get_object_or_404(User, id=sender_id)
        user_profile = get_object_or_404(UserProfile, user=user)
        user_profile_cart_products = UserProfileCart.objects.filter(user_profile=user_profile)

        all_selected = False
        is_selected = False
        total = Decimal(0.00)

        if all:
            if user_profile_cart_products.filter(is_selected=True).count() == user_profile_cart_products.count():
                for cart_product in user_profile_cart_products:
                    cart_product.is_selected = False
                    cart_product.save()
                message = "All Cart Products successfully unselected"
            else:
                for cart_product in user_profile_cart_products:
                    cart_product.is_selected = True
                    cart_product.save()
                message = "All Cart Products successfully selected"
        else:
            cart = get_object_or_404(UserProfileCart, id=cart_id, user_profile=user_profile)
            if cart.is_selected:
                cart.is_selected = False
                cart.save()
                message = "Cart Product successfully unselected"
            else:
                cart.is_selected = True
                cart.save()
                is_selected = True
                message = "Cart Product successfully selected"

        if user_profile_cart_products.filter(is_selected=True).count() == user_profile_cart_products.count():
            all_selected = True

        cart_products_selected_posters = []

        for user_profile_cart in UserProfileCart.objects.filter(user_profile=user_profile):
            if user_profile_cart.is_selected:
                cart_products_selected_posters.append(user_profile_cart.product.product_poster.first().photo.url)
                total += user_profile_cart.product.price * user_profile_cart.quantity

        data = {
            "success": True,
            "message": message,
            "all_selected": all_selected,
            "is_selected": is_selected,
            "selected_products_count": user_profile_cart_products.filter(is_selected=True).count(),
            "cart_products_selected_posters": cart_products_selected_posters, 
            "total": total
        }
        return JsonResponse(data, safe=False)
    return redirect("home")

def LikeProductFormView(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        sender_id = data.get("sender_id")
        product_id = data.get("product_id")

        user = get_object_or_404(User, id=sender_id)
        product = get_object_or_404(Product, id=product_id)
        user_profile = get_object_or_404(UserProfile, user=user)
        
        user_profile_favorite = UserProfileFavorite.objects.all().filter(user_profile=user_profile, product=product).first()
        if user_profile_favorite is None:
            user_profile_favorite = UserProfileFavorite(user_profile=user_profile, product=product)
            user_profile_favorite.save()
        
            data = {
                "success": True,
                "message": "Product successfully added to wishlist",
                "is_liked": True,
                "is_removed": False,
            }
        else:
            user_profile_favorite.delete()
            data = {
                "success": True,
                "message": "Product successfully removed from wishlist",
                "is_liked": False,
                "is_removed": True,
            }
        return JsonResponse(data, safe=False)
    return redirect("home")

def SubscribeStoreFormView(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        sender_id = data.get("sender_id")
        store_id = data.get("store_id")

        user = get_object_or_404(User, id=sender_id)
        store = get_object_or_404(Store, id=store_id)
        user_profile = get_object_or_404(UserProfile, user=user)
        
        user_profile_favorite, is_subscribed = UserProfileFavorite.objects.get_or_create(user_profile=user_profile, store=store)

        if not is_subscribed:
            user_profile_favorite.delete()

        subscribers = UserProfileFavorite.objects.filter(store=store).count()
        subscribers_text = f"{subscribers} {'subscribers' if subscribers > 1 else 'subscriber'}"

        data = {
            "success": True,
            "message": "Store successfully added to subscriptions",
            "is_subscribed": is_subscribed,
            "subscribers": subscribers,
            "text": subscribers_text,
        }
        return JsonResponse(data, safe=False)
    return redirect("home")

def LikeReviewFormView(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        sender_id = data.get("sender_id")
        review_id = data.get("review_id")

        user = get_object_or_404(User, id=sender_id)
        review = get_object_or_404(Review, id=review_id)
        user_profile = get_object_or_404(UserProfile, user=user)
        
        user_profile_favorite = UserProfileFavorite.objects.all().filter(user_profile=user_profile, review=review).first()
        if user_profile_favorite is None:
            user_profile_favorite = UserProfileFavorite(user_profile=user_profile, review=review)
            user_profile_favorite.save()
        
            data = {
                "success": True,
                "message": "Review successfully added to wishlist",
                "is_liked": True,
                "is_removed": False,
                "likes": review.user_profile_favorite_review.all().count(),
            }
        else:
            user_profile_favorite.delete()
            data = {
                "success": True,
                "message": "Review successfully removed from wishlist",
                "is_liked": False,
                "is_removed": True,
                "likes": review.user_profile_favorite_review.all().count(),
            }
        return JsonResponse(data, safe=False)
    return redirect("home")

def AddToCartFormView(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        sender_id = data.get("sender_id")
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        user = get_object_or_404(User, id=sender_id)
        product = get_object_or_404(Product, id=product_id)
        user_profile = get_object_or_404(UserProfile, user=user)

        user_profile_cart, is_added = UserProfileCart.objects.get_or_create(user_profile=user_profile, product=product, defaults={'quantity': quantity})

        if not is_added:
            user_profile_cart.quantity = quantity

        data = {
            "success": True,
            "message": "Product successfully added to cart",
            "cart_id": user_profile_cart.id,
            "is_added": is_added,
        }
        return JsonResponse(data, safe=False)
    return redirect("home")

def SendReviewFormView(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        sender_id = data.get("sender_id")
        product_id = data.get("product_id")
        rating = data.get("rating")
        comment = data.get("comment")

        user = get_object_or_404(User, id=sender_id)
        product = get_object_or_404(Product, id=product_id)

        review = Review(sender=user, product=product, rating=rating, comment=comment)
        review.save()

        data = {
            "success": True,
            "message": "Review successfully sended to product",
        }
        return JsonResponse(data, safe=False)
    return redirect("home")

def LogInFormView(request):
    if request.method == "POST" and not request.user.is_authenticated:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        user = None
        is_password = False 
        is_email = False

        if email and password:
            try:
                email_validator(email)
                try:
                    user = User.objects.get(email=email)
                    if user.check_password(password):
                        user = user
                    else:
                        user = None
                        is_password = True
                except User.DoesNotExist:
                    is_email = True

                if user is not None:
                    login(request, user)

                    data = {
                        "success": True,
                        "message": "User successfully authenticated",
                    }
                else:
                    data = {
                        "success": False,
                        "is_password": is_password,
                        "is_email": is_email,
                    }
                    if is_email:
                        data["message"] = "Account with this email does not exist"
                    else:
                        if is_password:
                            data["message"] = "Incorrect password"
            except ValidationError:
                data = {
                    "success": False,
                    "message": "Invalid email",
                    "is_email": True,
                }
        else:
            data = {
                "success": False, 
                "message": "This field can not be empty",
                "is_empty": True,
            }
            if not email:
                data["is_email"] = True
            if not password:
                data["is_password"] = True
        return JsonResponse(data, safe=False)
    return redirect("home")

def SignUpFormView(request):
    if request.method == "POST" and not request.user.is_authenticated:
        data = json.loads(request.body)
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if name and email and password and confirm_password:
            try:
                email_validator(email)
                if User.objects.filter(email=email).exists():
                    data = {
                        "success": False,
                        "message": "Account with this email already exists",
                        "is_email": True,
                    }
                else:
                    if password == confirm_password:
                        user = User(name=name, email=email)
                        user.set_password(password)
                        user.save()
                        login(request, user)
                        data = {
                            "success": True,
                            "message": "Account successfully created",
                        }
                    else:
                        data = {
                            "success": False,
                            "message": "Password does not match",
                            "is_password_confirm": True,
                        }
            except ValidationError:
                data = {
                    "success": False,
                    "message": "Invalid email",
                    "is_email": True,
                }
        else:
            data = {
                "success": False,
                "message": "This field can not be empty",
                "is_empty": True,
            }
            if not name:
                data["is_name"] = True
            if not email:
                data["is_email"] = True
            if not password:
                data["is_password"] = True
            if not confirm_password:
                data["is_password_confirm"] = True
        return JsonResponse(data, safe=False)
    return redirect("home")