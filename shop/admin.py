from django.contrib import admin
from .models import Category, Medicine, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "in_stock", "needs_prescription")
    list_editable = ("price", "in_stock")
    list_filter = ("category", "needs_prescription")
    search_fields = ("name", "maker")


class ItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("medicine", "price", "qty")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("__str__", "name", "phone", "total", "status", "created")
    list_editable = ("status",)
    list_filter = ("status",)
    inlines = [ItemInline]
