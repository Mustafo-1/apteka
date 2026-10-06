from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("dori/<int:pk>/", views.detail, name="detail"),
    path("savat/", views.cart, name="cart"),
    path("savat/<int:pk>/", views.cart_set, name="cart_set"),
    path("buyurtma/", views.checkout, name="checkout"),
]
