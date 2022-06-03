from django.db import router
from django.urls import path,include

from .views import AddIngredients, CartView, InventoryItemsView, UserLogin,UserRegister,BakeryItemView ,InventoryView,InventoryItemsView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("bakery-item",BakeryItemView,basename="item")
router.register("inventory",InventoryView,basename="inventory")
router.register("inventory-items",InventoryItemsView,basename="inventory-items")
router.register("cart",CartView,basename="cart")

urlpatterns = [
    path('user/register/',UserRegister.as_view(),name="register"),
    path('user/login/',UserLogin.as_view(),name="login"),
    path('user/add-ingredient/',AddIngredients.as_view(),name="add-ingredient"),
    path('user/',include(router.urls))
]
