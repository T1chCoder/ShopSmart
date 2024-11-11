from django.contrib import admin
from .models import *
from .forms import *
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.forms.widgets import Media
from django.db import models
from django.conf import settings

class DefaultAdmin(admin.ModelAdmin):
    ordering = ["created"]
    date_hierarchy = "created"
    list_per_page = 7

    @staticmethod
    def PhotoPreview(photo):
        if photo:
            return mark_safe("<img src='{url}' style='border-radius: 2px;' width='24px' height='24px' />".format(url=photo.url))

    @staticmethod
    def ShortenText(text, max):
        outlet = ""
        if (text != None):
            if sum(1 for char in text if char.isalpha()) < max:
                outlet += f"{text}"
            else:
                outlet += f"{text[:max]}..."
        else:
            outlet += "-"
        return outlet

class UserPassport(admin.TabularInline):
    model = UserPassport
    fk_name = "user"
    extra = 1
    fields = ("number", "issuance_date", "authority")
    verbose_name = "Passport"
    verbose_name_plural = "Passports"
    readonly_fields = ("user", "updated", "created")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("user",)
        return self.readonly_fields

@admin.register(User)
class UserAdmin(DefaultAdmin):
    inlines = [UserPassport]
    list_display = ["username", "name", "patronymic", "surname", "email", "phone", "photo_preview", "gender", "birthday", "is_superuser", "is_staff", "is_active", "last_login", "updated", "created"]
    list_filter = ["birthday", "gender", "is_superuser", "is_staff", "is_active", "updated", "created"]
    search_fields = ["id", "username", "email"]
    actions = ["make_superuser", "make_staff", "make_active", "ban", "delete"]
    fieldsets = [
        ("Edit", {"fields": ["name", "patronymic", "surname", "username", "email", "phone", "gender", "birthday"]}),
        ("More", {"fields": ["photo", "user_permissions"]}),
    ]

    def full_name(self, obj):
        return obj.full_name()

    def make_superuser(self, request, queryset):
        queryset.update(is_superuser=True)
        queryset.update(is_staff=True)
        queryset.update(is_active=True)

    def make_staff(self, request, queryset):
        queryset.update(is_superuser=False)
        queryset.update(is_staff=True)
        queryset.update(is_active=True)

    def make_active(self, request, queryset):
        queryset.update(is_superuser=False)
        queryset.update(is_staff=False)
        queryset.update(is_active=True)

    def ban(self, request, queryset):
        queryset.update(is_superuser=False)
        queryset.update(is_staff=False)
        queryset.update(is_active=False)

    def delete(self, request, queryset):
        queryset.delete()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def photo_preview(self, obj):
        return self.PhotoPreview(obj.photo)

    make_superuser.short_description = f"Make selected {User._meta.verbose_name_plural} admin"
    make_staff.short_description = f"Make selected {User._meta.verbose_name_plural} an employee"
    make_active.short_description = f"Make selected {User._meta.verbose_name_plural} a client"
    delete.short_description = f"Delete selected {User._meta.verbose_name_plural}"
    ban.short_description = f"Ban selected {User._meta.verbose_name_plural}"
    full_name.short_description = f"Full name"
    photo_preview.short_description = f"Photo"

class StoreOwnerAdmin(admin.TabularInline):
    model = StoreOwner
    fk_name = "store"
    extra = 1
    fields = ("user", "is_admin", "is_active")
    verbose_name = "Owner"
    verbose_name_plural = "Owners"
    readonly_fields = ("store", "updated", "created")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("store",)
        return self.readonly_fields

@admin.register(Store)
class StoreAdmin(DefaultAdmin):
    inlines = [StoreOwnerAdmin]
    list_display = ["title", "photo_preview", "rating", "subscribers", "orders", "updated", "created"]
    list_filter = ["rating", "subscribers", "orders", "updated", "created"]
    search_fields = ["id", "title"]
    fieldsets = [
        ("Edit", {"fields": ["title", "photo"]}),
    ]

    def photo_preview(self, obj):
        return self.PhotoPreview(obj.photo)

    photo_preview.short_description = f"Photo"
    
@admin.register(StoreReport)
class StoreReportAdmin(DefaultAdmin):
    list_display = ["store", "sender", "text", "updated", "created"]
    list_filter = ["store", "sender", "updated", "created"]
    search_fields = ["id", "store__title", "sender__username"]
    fieldsets = [
        ("Edit", {"fields": ["store", "text"]}),
    ]

    def save_model(self, request, obj, form, change):
        if not change and request.user:
            obj.sender = request.user
        obj.save()

@admin.register(Chat)
class ChatAdmin(DefaultAdmin):
    list_display = ["store", "client", "updated", "created"]
    list_filter = ["store", "client", "updated", "created"]
    search_fields = ["id", "store__title", "client__username"]
    fieldsets = [
        ("Edits", {"fields": ["store"]}),
    ]

    def save_model(self, request, obj, form, change):
        if not change and request.user:
            obj.client = request.user
        obj.save()

@admin.register(ChatMessage)
class ChatMessageAdmin(DefaultAdmin):
    list_display = ["chat", "sender", "text", "updated", "created"]
    list_filter = ["sender", "updated", "created"]
    search_fields = ["id", "sender__username"]
    fieldsets = [
        ("Edit", {"fields": ["chat", "text"]}),
    ]

    def save_model(self, request, obj, form, change):
        if not change and request.user:
            obj.sender = request.user
        obj.save()

@admin.register(Category)
class CategoryAdmin(DefaultAdmin):
    list_display = ["title", "pre_category", "updated", "created"]
    list_filter = ["updated", "created"]
    search_fields = ["id", "title", "pre_category__title"]
    fieldsets = [
        ("Edit", {"fields": ["pre_category", "title"]}),
    ]

@admin.register(Banner)
class BannerAdmin(DefaultAdmin):
    list_display = ["publisher", "photo_preview", "updated", "created"]
    list_filter = ["publisher", "updated", "created"]
    search_fields = ["id", "publisher__username", "id"]
    fieldsets = [
        ("Edit", {"fields": ["photo", "url"]}),
    ]

    def photo_preview(self, obj):
        return self.PhotoPreview(obj.photo)

    def save_model(self, request, obj, form, change):
        if not change and request.user:
            obj.publisher = request.user
        obj.save()

    photo_preview.short_description = f"Photo"

class ProductPosterAdmin(admin.TabularInline):
    model = ProductPoster
    fk_name = "product"
    extra = 1
    fields = ("photo",)
    verbose_name = "Poster"
    verbose_name_plural = "Posters"
    readonly_fields = ("product", "updated", "created")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("product",)
        return self.readonly_fields

@admin.register(Product)
class ProductAdmin(DefaultAdmin):
    inlines = [ProductPosterAdmin]
    list_display = ["title", "store", "category", "description", "price", "discount", "rating", "bought", "reviews", "is_popular", "is_hot", "is_active", "updated", "created"]
    list_filter = ["store", "category", "price", "discount", "stock", "rating", "bought", "reviews", "is_popular", "is_hot", "is_active", "updated", "created"]
    search_fields = ["id", "title", "store__title", "category__title", "description", "price", "discount", "bought", "reviews"]
    fieldsets = [
        ("Edits", {"fields": ["store", "category", "title", "description", "act_price", "discount", "stock", "is_popular", "is_hot"]}),
    ]

@admin.register(Review)
class ProductReviewAdmin(DefaultAdmin):
    list_display = ["product", "sender", "rating", "text", "is_active", "updated", "created"]
    list_filter = ["product", "sender", "rating", "is_active", "updated", "created"]
    search_fields = ["id", "product__title", "sender__username", "comment"]
    fieldsets = [
        ("Edits", {"fields": ["product", "rating", "comment"]}),
    ]

    def text(self, obj):
        return self.ShortenText(obj.comment, max=18)

    def save_model(self, request, obj, form, change):
        if not change and request.user:
            obj.sender = request.user
        obj.save()

    text.short_description = f"Comment"

@admin.register(ProductReport)
class ProductReportAdmin(DefaultAdmin):
    list_display = ["product", "sender", "text", "updated", "created"]
    list_filter = ["product", "sender", "updated", "created"]
    search_fields = ["id", "product__title", "sender__username", "text"]
    fieldsets = [
        ("Edit", {"fields": ["product", "text"]}),
    ]

    def save_model(self, request, obj, form, change):
        if not change and request.user:
            obj.sender = request.user
        obj.save()

class OrderProductAdmin(admin.TabularInline):
    model = OrderProduct
    fk_name = "order"
    extra = 1
    fields = ("product", "quantity", "sum",)
    verbose_name = "Product"
    verbose_name_plural = "Products"
    readonly_fields = ("order", "sum", "updated", "created")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("order",)
        return self.readonly_fields

class OrderStatusAdmin(admin.TabularInline):
    model = OrderStatus
    fk_name = "order"
    extra = 1
    fields = ("status",)
    verbose_name = "Status"
    verbose_name_plural = "Statuses"
    readonly_fields = ("order", "updated", "created")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("order",)
        return self.readonly_fields

class OrderCancelAdmin(admin.TabularInline):
    model = OrderCancel
    fk_name = "order"
    extra = 1
    fields = ("comment",)
    verbose_name = "Cancel"
    verbose_name_plural = "Cancels"
    readonly_fields = ("order", "updated", "created")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("order",)
        return self.readonly_fields

@admin.register(Order)
class OrderAdmin(DefaultAdmin):
    inlines = [OrderProductAdmin, OrderStatusAdmin, OrderCancelAdmin]
    list_display = ["customer", "total", "updated", "created"]
    list_filter = ["is_pending", "is_shifted", "is_delivered", "is_paid", "is_cancelled", "updated", "created"]
    search_fields = ["id", "customer__username", "total"]

    def save_model(self, request, obj, form, change):
        if not change and request.user:
            obj.customer = request.user
        obj.save()

class UserProfileCartAdmin(admin.TabularInline):
    model = UserProfileCart
    fk_name = "user_profile"
    extra = 1
    fields = ("product", "quantity", "is_selected",)
    verbose_name = "Product"
    verbose_name_plural = "Cart"
    readonly_fields = ("user_profile", "updated", "created")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("user_profile",)
        return self.readonly_fields

@admin.register(UserProfile)
class UserProfileAdmin(DefaultAdmin):
    inlines = [UserProfileCartAdmin]
    list_display = ["user", "language", "currency", "updated", "created"]
    list_filter = ["language", "currency", "updated", "created"]
    search_fields = ["id", "user__username"]
    fieldsets = [
        ("Edit", {"fields": ["language"]}),
    ]

admin.site.site_title = settings.WEBSITE_NAME
admin.site.site_header = f"The admin panel of {settings.WEBSITE_NAME}"
admin.site.index_title = "Welcome to the admin panel"