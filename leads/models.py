from django.db import models
from django.contrib.auth.models import *
from django.db.models.signals import *
from .validators import *
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from datetime import datetime
from django.dispatch import receiver
import os
import uuid
from decimal import Decimal
from leads.choices import *
from django.db.models import Avg
from django.utils import timezone
from django.db import transaction

def user_photo_path(instance, filename):
    return os.path.join("images/user/", datetime.now().date().strftime("%Y/%m/%d"), filename)

def store_photo_path(instance, filename):
    return os.path.join("images/store/", datetime.now().date().strftime("%Y/%m/%d"), filename)

def product_photo_path(instance, filename):
    return os.path.join("images/product/", datetime.now().date().strftime("%Y/%m/%d"), filename)

def banner_photo_path(instance, filename):
    return os.path.join("images/banner/", datetime.now().date().strftime("%Y/%m/%d"), filename)

class User(AbstractUser):
    date_joined = None
    first_name = None 
    last_name = None
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    custom_id = models.IntegerField("Short ID", unique=True, editable=False, blank=False, null=True)
    name = models.CharField("Name", max_length=250, blank=False, null=True)
    patronymic = models.CharField("Patronymic", max_length=250, blank=True, null=True)
    surname = models.CharField("Surname", max_length=250, blank=False, null=True)
    phone = models.CharField("Phone", max_length=250, blank=True, null=True)
    photo = models.ImageField("Photo", upload_to=user_photo_path, blank=True, null=True)
    birthday = models.DateField("Birthday", blank=False, null=True)
    gender = models.CharField("Gender", max_length=150, choices=(("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other")), blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def save(self, *args, **kwargs):
        if not self.custom_id:
            last_record = User.objects.all().order_by('-custom_id').first()
            if not last_record:
                last_record = 0
            self.custom_id = (last_record.custom_id + 1) if last_record else 1 
        if not self.username:
            self.username = f"{self.name}-{self.custom_id}"
        return super().save(*args, **kwargs)

    def full_name(self):
        return f"{' ' + self.name if self.name else ''}{' ' + self.patronymic if self.patronymic else ''}{' ' + self.surname if self.surname else ''}"

    def __str__(self):
        return f"{self.username}"

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

class UserPassport(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    user = models.OneToOneField(User, verbose_name=User._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_passport")
    number = models.CharField("Number", max_length=250, blank=False, null=True)
    issuance_date = models.DateField("Issuance date", blank=False, null=True)
    authority = models.CharField("Authority", max_length=250, blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        db_table = "user_passports"
        verbose_name = "User passport"
        verbose_name_plural = "User passports"

class Store(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    title = models.CharField("Title", max_length=250, blank=False, null=True)
    photo = models.ImageField("Photo", upload_to=store_photo_path, blank=False, null=True)
    rating = models.FloatField("Rating", default=0, editable=False, blank=False, null=True)
    orders = models.IntegerField("Orders", default=0, editable=False, blank=False, null=True)
    subscribers = models.IntegerField("Subscribers", default=0, editable=False, blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "stores"
        verbose_name = "Store"
        verbose_name_plural = "Stores"

class StoreOwner(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    store = models.ForeignKey(Store, verbose_name="Store", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="store_owner")
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, blank=False, null=True, related_name="store_owner_user")
    is_admin = models.BooleanField("Admin", default=False, blank=False, null=False)
    is_active = models.BooleanField("Active", default=True, blank=False, null=False)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "store_owners"
        verbose_name = "Store owner"
        verbose_name_plural = "Store owners"

class StoreReport(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    store = models.ForeignKey(Store, verbose_name="Store", on_delete=models.CASCADE, blank=False, null=True, related_name="store_report")
    sender = models.ForeignKey(User, verbose_name="Sender", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="store_report_sender")
    text = models.TextField("Text", blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "store_reports"
        verbose_name = "Store report"
        verbose_name_plural = "Store reports"

class Chat(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    store = models.ForeignKey(Store, verbose_name="Store", on_delete=models.CASCADE, blank=False, null=True, related_name="chat_store")
    client = models.ForeignKey(User, verbose_name="Client", on_delete=models.CASCADE, blank=False, null=True, related_name="chat_client")
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self.store.title} - {self.client.username}"

    class Meta:
        db_table = "chats"
        verbose_name = "Chat"
        verbose_name_plural = "Chats"

class ChatMessage(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    chat = models.ForeignKey(Chat, verbose_name="Chat", on_delete=models.CASCADE, blank=False, null=True, related_name="chat_message")
    sender = models.ForeignKey(User, verbose_name="Sender", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="chat_message_sender")
    text = models.TextField("Text", blank=False, null=True)
    is_store = models.BooleanField("Store", default=False, editable=False, blank=False, null=False)
    is_client = models.BooleanField("Client", default=False, editable=False, blank=False, null=False)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "chat_messages"
        verbose_name = "Message"
        verbose_name_plural = "Messages"

class Category(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    pre_category = models.ForeignKey("self", verbose_name="Pre-category", on_delete=models.CASCADE, blank=True, null=True, related_name="category_pre_category")
    title = models.CharField("Title", max_length=250, blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Banner(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    publisher = models.ForeignKey(User, verbose_name="Publisher", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="banner_publisher")
    photo = models.ImageField("Photo", upload_to=banner_photo_path, blank=False, null=True)
    url = models.SlugField("URL", blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "banners"
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

class Product(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    store = models.ForeignKey(Store, verbose_name="Store", on_delete=models.CASCADE, blank=False, null=True, related_name="product_store")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE, blank=False, null=True, related_name="product_category")
    title = models.CharField("Title", max_length=250, blank=False, null=True)
    description = models.TextField("Description", blank=False, null=True)
    act_price = models.DecimalField("Act-price", default=5.0, max_digits=10, decimal_places=2, blank=False, null=True)
    price = models.DecimalField("Price", default=5.0, max_digits=10, decimal_places=2, editable=False, blank=False, null=True)
    stock = models.IntegerField("Stock", default=1, blank=False, null=True)
    discount = models.IntegerField("Discount", default=0, validators=[MaxValueValidator(100)], blank=False, null=True)
    rating = models.FloatField("Rating", default=0.0, editable=False, blank=False, null=True)
    bought = models.IntegerField("Bought", default=0, editable=False, blank=False, null=True)
    reviews = models.IntegerField("Reviews", default=0, editable=False, blank=False, null=True)
    is_hot = models.BooleanField("Hot", default=False, blank=False, null=False)
    is_popular = models.BooleanField("Popular", default=False, blank=False, null=False)
    is_active = models.BooleanField("Posted", default=True, blank=False, null=False)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def save(self, *args, **kwargs):
        self.price = self.act_price - self.act_price * (Decimal(self.discount) / Decimal(100))
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

class ProductAttribute(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="product_attribute")
    variable = models.CharField("Variable", choices=PRODUCT_ATTRIBUTE_CHOICES, max_length=250, blank=False, null=True)
    value = models.CharField("Variable", max_length=250, blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "product_attributes"
        verbose_name = "Product attribute"
        verbose_name_plural = "Product attributes"

class ProductPoster(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="product_poster")
    photo = models.ImageField("Photo", upload_to=product_photo_path, blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "product_posters"
        verbose_name = "Product poster"
        verbose_name_plural = "Product posters"

class Review(models.Model):
    class Rating(models.IntegerChoices):
        VERY_BAD = 1, 'Very Bad'
        BAD = 2, 'Bad'
        AVERAGE = 3, 'Average'
        GOOD = 4, 'Good'
        EXCELLENT = 5, 'Excellent'

    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE, blank=False, null=True, related_name="review_product")
    sender = models.ForeignKey(User, verbose_name="Sender", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="review_sender")
    rating = models.IntegerField("Rating", choices=Rating.choices, blank=False, null=True)
    comment = models.TextField("Comment", blank=False, null=True)
    is_active = models.BooleanField("Posted", default=True, editable=False, blank=False, null=False)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def save(self, *args, **kwargs):
        product_reviews_rating = Product.objects.get(id=self.product.id).review_product.all().values_list("rating", flat=True)
        average_rating = product_reviews_rating.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            self.product.rating = round(average_rating * 2) / 2
        else:
            self.product.rating = 0
        self.product.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "reviews"
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

class ProductReport(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE, blank=False, null=True, related_name="product_report")
    sender = models.ForeignKey(User, verbose_name="Sender", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="product_report_sender")
    text = models.TextField("Text", blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "product_reports"
        verbose_name = "Product report"
        verbose_name_plural = "Product reports"

class Order(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    custom_id = models.IntegerField("Short ID", unique=True, editable=False, blank=False, null=True)
    customer = models.ForeignKey(User, verbose_name="Customer", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="order_customer")
    address = models.CharField("Address", max_length=250, blank=False, null=True)
    total = models.DecimalField("Total", max_digits=10, decimal_places=2, editable=False, blank=False, null=True)
    delivery_date = models.DateTimeField("Delivery date", editable=False, blank=True, null=True)
    is_pending = models.BooleanField("Pending", editable=False, default=False, blank=False, null=False)
    is_shifted = models.BooleanField("Shifted", editable=False, default=False, blank=False, null=False)
    is_delivered = models.BooleanField("Delivered", editable=False, default=False, blank=False, null=False)
    is_paid = models.BooleanField("Paid", editable=False, default=False, blank=False, null=False)
    is_cancelled = models.BooleanField("Cancelled", editable=False, default=False, blank=False, null=False)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def status(self):
        if self.is_paid:
            return "Issued to the buyer"
        else:
            if self.is_cancelled:
                return "Cancelled by the buyer"
            else:
                if self.is_delivered:
                    return "Awaiting Collection"
                else:
                    if self.is_shifted:
                        return "On the Way"
                    else:
                        return "Awaiting Processing" 

    def save(self, *args, **kwargs):
        if not self.custom_id:
            last_record = Order.objects.all().order_by('-custom_id').first()
            if not last_record:
                last_record = 0
            self.custom_id = (last_record.custom_id + 1) if last_record else 1 
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class OrderProduct(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    order = models.ForeignKey(Order, verbose_name="Order", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="order_product")
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE, blank=False, null=True, related_name="order_produc_item")
    quantity = models.IntegerField("Quantity", blank=False, null=True)
    sum = models.DecimalField("Sum", max_digits=10, decimal_places=2, editable=False, blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def save(self, *args, **kwargs):
        order = Order.objects.get(id=self.order.id)
        order_products = OrderProduct.objects.filter(order=order)
        total = Decimal(0.00)
        for order_product in order_products:
            sum = order_product.sum or order_product.product.price
            total += sum * order_product.quantity
        order.total = total
        order.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "order_products"
        verbose_name = "Order product"
        verbose_name_plural = "Order products"

class OrderStatus(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    order = models.ForeignKey(Order, verbose_name="Order", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="order_status")
    status = models.CharField("Status", max_length=250, choices=[("PENDING", "Pending"), ("SHIPPED", "Shipped"), ("DELIVERED", "Delivered"), ("PAID", "Paid")], blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def save(self, *args, **kwargs):
        if self.status == "PENDING":
            self.order.is_pending = True
        if self.status == "SHIPPED":
            self.order.is_shifted = True
        if self.status == "DELIVERED":
            self.order.delivery_date = self.created or timezone.now()
            self.order.is_delivered = True
        if self.status == "PAID":
            self.order.is_paid = True
        self.order.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "order_statuses"
        verbose_name = "Order status"
        verbose_name_plural = "Order statuses"

class OrderCancel(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    order = models.ForeignKey(Order, verbose_name="Order", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="order_cancel")
    comment = models.TextField("Comment", blank=True, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def save(self, *args, **kwargs):
        self.order.is_cancelled = True
        self.order.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "order_cancels"
        verbose_name = "Order cancel"
        verbose_name_plural = "Order cancels"

class UserProfile(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    user = models.OneToOneField(User, verbose_name=User._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile")
    language = models.CharField("Language", max_length=250, choices=LANGUAGE_CHOICES, default="RUSSIAN", blank=False, null=True)
    currency = models.CharField("Currency", max_length=250, choices=CURRENCY_CHOICES, default="RUB", editable=False, blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        db_table = "user_profiles"
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"

class UserProfileDeliveryAddress(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    user_profile = models.ForeignKey(UserProfile, verbose_name=UserProfile._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile_delivery_address")  
    text = models.CharField("Text", max_length=250, blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "user_profile_delivery_addresses"
        verbose_name = "User profile delivery address"
        verbose_name_plural = "User profile delivery addresses"

class UserProfileSavedCard(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    user_profile = models.ForeignKey(UserProfile, verbose_name=UserProfile._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile_saved_card")  
    number = models.CharField("Number", max_length=16, blank=False, null=True)
    expiration = models.DateField("Expiration", blank=False, null=True)
    cvv = models.CharField("CVV", max_length=4, blank=False, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "user_profile_saved_cards"
        verbose_name = "User profile saved card"
        verbose_name_plural = "User profile saved cards"

class UserProfileFavorite(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    user_profile = models.ForeignKey(UserProfile, verbose_name=UserProfile._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile_favorite")
    store = models.ForeignKey(Store, verbose_name=Store._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile_favorite_store")
    product = models.ForeignKey(Product, verbose_name=Product._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile_favorite_product")
    review = models.ForeignKey(Review, verbose_name=Review._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile_favorite_review")
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "user_profile_favorites"
        verbose_name = "User profile favorite"
        verbose_name_plural = "User profile favorites"

class UserProfileHistory(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    user_profile = models.ForeignKey(UserProfile, verbose_name=UserProfile._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile_history")
    store = models.ForeignKey(Store, verbose_name=Store._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile_history_store")
    category = models.ForeignKey(Category, verbose_name=Category._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile_history_category")
    product = models.ForeignKey(Product, verbose_name=Product._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile_history_product")
    search = models.CharField("Search", max_length=250, editable=False, blank=True, null=True)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "user_profile_histories"
        verbose_name = "User profile history"
        verbose_name_plural = "User profile histories"

class UserProfileCart(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    user_profile = models.ForeignKey(UserProfile, verbose_name=UserProfile._meta.verbose_name, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user_profile_cart")
    product = models.ForeignKey(Product, verbose_name=Product._meta.verbose_name, on_delete=models.CASCADE, blank=False, null=True, related_name="user_profile_cart_product")
    quantity = models.IntegerField("Quantity", blank=False, null=True)
    sum = models.DecimalField("Sum", default=5.0, max_digits=10, decimal_places=2, blank=False, null=True)
    total = models.DecimalField("Total", default=5.0, max_digits=10, decimal_places=2, editable=False, blank=False, null=True)
    is_selected = models.BooleanField("Selected", default=True, blank=False, null=False)
    # More
    updated = models.DateTimeField("Updated", auto_now=True, editable=False, blank=False, null=True)
    created = models.DateTimeField("Created", auto_now_add=True, editable=False, blank=False, null=True)

    def save(self, *args, **kwargs):
        self.sum = self.quantity * self.product.price
        self.total = self.quantity * self.product.act_price
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    class Meta:
        db_table = "user_profile_cart_products"
        verbose_name = "User profile cart product"
        verbose_name_plural = "User profile cart products"

@receiver(post_save, sender=User)
def user_signals(sender, instance, created, **kwargs):
    if created:
        UserPassport.objects.create(user=instance)
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=Review)
def user_signals(sender, instance, created, **kwargs):
    if created:
        product_reviews_rating = Product.objects.get(id=instance.product.id).review_product.all().values_list("rating", flat=True)
        average_rating = product_reviews_rating.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            instance.product.rating = round(average_rating * 2) / 2
        else:
            instance.product.rating = 0
        instance.product.save()

@receiver(post_delete, sender=Review)
def review_delete_signals(sender, instance, **kwargs):
    product_reviews_rating = Product.objects.get(id=instance.product.id).review_product.all().values_list("rating", flat=True)
    average_rating = product_reviews_rating.aggregate(Avg('rating'))['rating__avg']
    if average_rating is not None:
        instance.product.rating = round(average_rating * 2) / 2
    else:
        instance.product.rating = 0
    instance.product.save()

@receiver(post_delete, sender=OrderProduct)
def order_product_delete_signals(sender, instance, **kwargs):
    try:
        order = Order.objects.get(id=instance.order.id)
        order_products = OrderProduct.objects.filter(order=order).exclude(id=instance.id)
        total = Decimal(0.00)
        for order_product in order_products:
            sum = order_product.sum or order_product.product.price
            total += sum * order_product.quantity
        order.total = total
        order.save()
    except:
        pass
    
@receiver(post_save, sender=OrderProduct)
def order_product_signals(sender, instance, created, **kwargs):
    if created:
        instance.sum = instance.product.price
        transaction.on_commit(lambda: instance.save(update_fields=['sum']))