from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"tables", views.BookingViewSet, basename="booking")

urlpatterns = [
    path("", views.index, name="index"),
    path("menu/", views.MenuItemsView.as_view(), name="menu-items"),
    path("menu/<int:pk>", views.SingleMenuItemView.as_view(), name="single-menu-item"),
    path("booking/", include(router.urls)),  # -> /restaurant/booking/tables/
]
