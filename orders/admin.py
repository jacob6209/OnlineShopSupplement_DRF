from django.contrib import admin
from orders.models import OrderItem,Order
from django.db.models import Count


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity', 'unit_price']
    extra = 0
    min_num = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'datetime_created', 'num_of_items']
    list_editable = ['status']
    list_per_page = 10
    ordering = ['-datetime_created']
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        return super() \
                .get_queryset(request) \
                .prefetch_related('items') \
                .annotate(
                    items_count=Count('items')
                )

    @admin.display(ordering='items_count', description='# items')
    def num_of_items(self, order):
        return order.items_count

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    autocomplete_fields = ['product']
