from django.contrib import admin
from django.urls import include, path

from restaurant import views as restaurant_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Static index page
    path("", restaurant_views.index, name="home"),
    # Restaurant app (menu + booking API)
    path("restaurant/", include("restaurant.urls")),
    # Djoser: user registration/management and token auth
    path("auth/", include("djoser.urls")),                # /auth/users/, /auth/users/me/ ...
    path("auth/", include("djoser.urls.authtoken")),      # /auth/token/login/, /auth/token/logout/
]
