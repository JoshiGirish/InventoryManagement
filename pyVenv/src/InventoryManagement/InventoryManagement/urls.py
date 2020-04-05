from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from InvManage.views import *

urlpatterns = [
	path('create_product/',create_product_view, name='create_product'),
    path('vendor/', create_vendor_view, name='create_vendor'),
    path('create_purchase_order/', create_purchase_order_view, name='create_purchase_order'),
    path('update_product/<str:pk>/',update_product_view, name='update_product'),
    path('delete_product/', delete_product_view, name='delete_product'),
    path('products/',products_view, name='products'),
    path('upload/',uploadCSV, name='upload'),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)