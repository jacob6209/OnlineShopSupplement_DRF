from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from . import models
from .models import Product, ProductImage



class InventoryFilter(admin.SimpleListFilter):
    LESS_THAN_3 = '<3'
    BETWEEN_3_and_10 = '3<=10'
    MORE_THAN_10 = '>10'
    title = 'Critical Inventory Status'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            (InventoryFilter.LESS_THAN_3, 'low'),
            (InventoryFilter.BETWEEN_3_and_10, 'Medium'),
            (InventoryFilter.MORE_THAN_10, 'OK'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.LESS_THAN_3:
            return queryset.filter(inventory__lt=3)
        if self.value() == InventoryFilter.BETWEEN_3_and_10:
            return queryset.filter(inventory__range=(3, 10))
        if self.value() == InventoryFilter.MORE_THAN_10:
            return queryset.filter(inventory__gt=10)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

from django.utils.html import mark_safe
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','images_links','inventory','soled_item', 'unit_price','tags','inventory_status', 'product_category', 'num_of_comments']
    list_per_page = 10
    list_editable = ['unit_price']
    list_select_related = ['category']
    list_filter = ['datetime_created', InventoryFilter]
    actions = ['clear_inventory']
    search_fields = ['name', ]
    prepopulated_fields = {
        'slug': ['name', ]
    }
    inlines = [ProductImageInline]


    def images_links(self, obj):
        image_links = []
        for image in obj.images.all():
            image_links.append('<a href="{}">{}</a>'.format(image.image.url, image.image.name))
        if not image_links:
            return 'No Images'
        return mark_safe(", ".join(image_links))

    images_links.short_description = 'Images Links'

    # def images_preview(self, obj):
    #     images_html = ""
    #     for image in obj.images.all():
    #         images_html += '<img src="{}" width="100" height="100" />'.format(image.image.url)
    #     if not images_html:
    #         return 'No Images'
    #     return mark_safe(images_html)

    # images_preview.short_description = 'Images Preview'

    def get_queryset(self, request):
        return super().get_queryset(request) \
                .prefetch_related('comments') \
                .annotate(
                    comments_count=Count('comments'),
                )

    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        if product.inventory > 50:
            return 'High'
        return 'Medium'
    
    @admin.display(description='# comments', ordering='comments_count')
    def num_of_comments(self, product):
        url = (
            reverse('admin:store_comment_changelist') 
            + '?'
            + urlencode({
                'product__id': product.id,
            })
        )
        return format_html('<a href="{}">{}</a>', url, product.comments_count)
        
    
    @admin.display(ordering='category__title')
    def product_category(self, product):
        return product.category.title

    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} of products inventories cleared to zero.',
            messages.ERROR,
        )
    

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user','body','product', 'status','datetime_created' ]
    list_editable = ['status']
    list_per_page = 10
    autocomplete_fields = ['product', ]



admin.site.register(models.Category)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','phone_number', 'email', 'address']
    list_per_page = 10
    ordering = ['user__last_name', 'user__first_name', ]
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith', ]

    def first_name(self, customer):
        return customer.user.first_name
    
    def last_name(self, customer):
        return customer.user.last_name
    
    def phone_number(self, customer):
        return customer.phone_number

    def email(self, customer):
        return customer.user.email
    
    def address(self,customer):
        return f'{customer.Customeraddress.province},{customer.Customeraddress.city},{customer.Customeraddress.street}'





class CartItemInline(admin.TabularInline):
    model = models.CartItem
    fields = ['id', 'product', 'quantity']
    extra = 0
    min_num = 1


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    inlines = [CartItemInline]


admin.site.register(models.Ad)