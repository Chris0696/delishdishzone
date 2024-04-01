from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as Marketplaceviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('marketplace/', include('marketplace.urls')),

    # path('<slug:slug>/', views.foodListing, name='foodListing'),

    # CART
    path('cart/', Marketplaceviews.cart, name='cart'),

    # SEARCH
    path('search/', Marketplaceviews.search, name='search'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


