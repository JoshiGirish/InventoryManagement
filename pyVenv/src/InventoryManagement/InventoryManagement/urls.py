from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from InvManage.views import *

urlpatterns = [

    # Routes for managing company
    path('company/', create_company_view, name='company'),
    path('companies/', display_companies_view, name='companies'),
    path('company/<str:pk>/update', update_company_view, name='update_company'),
    path('company/<str:pk>/delete', delete_company_view, name='delete_company'),

    # Routes for managing products
    path('product/', create_product_view, name='product'),
    path('products/',display_products_view, name='products'),
    path('product/<str:pk>/update', update_product_view, name='update_product'),
    path('product/<str:pk>/delete', delete_product_view, name='delete_product'),

    # Routes for managing vendors
    path('vendor/', create_vendor_view, name='vendor'),
    path('vendors/', display_vendors_view, name='vendors'),
    path('vendor/<str:pk>/update', update_vendor_view, name='update_vendor'),
    path('vendor/<str:pk>/delete', delete_vendor_view, name='delete_vendor'),
    path('get_vendor/', get_vendor, name ='get_vendor'), # ajax call in create puchase order on vendor dropdown
    
    # Routes for managing POs
    path('purchase_order/', create_purchase_order_view, name='purchase_order'),
    path('purchase_orders/',display_purchase_orders_view, name='purchase_orders'),
    path('purchase_order/<str:pk>/update', update_purchase_order_view, name='update_purchase_order'),
    path('purchase_order/<str:pk>/delete', delete_purchase_order_view, name='delete_purchase_order'),
    path('purchase_order/<str:pk>/print',print_purchase_order_view, name='print_purchase_order'),

    path('upload/<data>/',uploadCSV, name='upload'),
    path('admin/', admin.site.urls),

    url(r'^api-auth/', include('rest_framework.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)