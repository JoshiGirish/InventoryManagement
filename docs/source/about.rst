About
===============

**INVENT** is a ``Django`` based RESTful web application. It implements modular and reusable code with clear separation of concerns using ``Model-Template-View`` architectural pattern.

- :doc:`Models </autoapi/InvManage/models/index>` describe the logical data structure.
- :doc:`Templates <https://github.com/JoshiGirish/InventoryManagement/tree/master/pyVenv/src/InventoryManagement/InvManage/templates>` represent static HTML fragments of the user interface.
- :doc:`Views </autoapi/InvManage/views/index>` are responsible for handling requests and deciding the response. 

In addition, the application uses `Django Forms API <https://docs.djangoproject.com/en/3.2/ref/forms/api>`_ and `Django REST framework <https://www.django-rest-framework.org>`_. Django Forms API allows hassle free rendering of web forms, while Django REST framework provides web browsable API, authentication, and serialization capabilities. See :doc:`Forms </autoapi/InvManage/forms/index>` and :doc:`Serializers </autoapi/InvManage/serializers/index>` sections of the documentation.

The application exposes the following endpoints, which are listed in the `urls.py <https://github.com/JoshiGirish/InventoryManagement/blob/master/pyVenv/src/InventoryManagement/InventoryManagement/urls.py>`_ file and documented in :doc:`Views </autoapi/InvManage/views/index>` section.::

	
    # Routes for managing company
    path('company/', create_company_view, name='company'),
    path('companies/', display_companies_view, name='companies'),
    path('company/update', update_company_view, name='update_company'),
    path('company/<str:pk>/delete', delete_company_view, name='delete_company'),

    # Routes for managing products
    path('product/', create_product_view, name='product'),
    path('products/',display_products_view, name='products'),
    path('product/update', update_product_view, name='update_product'),
    path('product/<str:pk>/delete', delete_product_view, name='delete_product'),

    # Routes for managing vendors
    path('vendor/', create_vendor_view, name='vendor'),
    path('vendors/', display_vendors_view, name='vendors'),
    path('vendor/update', update_vendor_view, name='update_vendor'),
    path('vendor/<str:pk>/delete', delete_vendor_view, name='delete_vendor'),
    path('get_vendor/', get_vendor, name ='get_vendor'), # ajax call in create puchase order on vendor dropdown
    
    # Routes for managing consumers
    path('consumer/', create_consumer_view, name='consumer'),
    path('consumers/', display_consumers_view, name='consumers'),
    path('consumer/update', update_consumer_view, name='update_consumer'),
    path('consumer/<str:pk>/delete', delete_consumer_view, name='delete_consumer'),
    path('get_consumer/', get_consumer, name ='get_consumer'), # ajax call in create sales order on consumer dropdown
    
    # Routes for managing GRNs
    path('grn/', create_grn_view, name='grn'),
    path('grns/',display_grns_view, name='grns'),
    path('grn/update', update_grn_view, name='update_grn'),
    path('grn/<str:pk>/delete', delete_grn_view, name='delete_grn'),
    path('grn/<str:pk>/print',print_grn_view, name='print_grn'),

    # Routes for managing POs
    path('purchase_order/', create_purchase_order_view, name='purchase_order'),
    path('purchase_orders/',display_purchase_orders_view, name='purchase_orders'),
    path('purchase_order/update', update_purchase_order_view, name='update_purchase_order'),
    path('purchase_order/<str:pk>/delete', delete_purchase_order_view, name='delete_purchase_order'),
    path('purchase_order/<str:pk>/print',print_purchase_order_view, name='print_purchase_order'),
    path('product_purchase_entries/', get_product_purchase_entries_view, name='product_purchase_entries'), # JSON API to get PPEs of POs
    
    # Routes for managing SOs
    path('sales_order/', create_sales_order_view, name='sales_order'),
    path('sales_orders/',display_sales_orders_view, name='sales_orders'),
    path('sales_order/update', update_sales_order_view, name='update_sales_order'),
    path('sales_order/<str:pk>/delete', delete_sales_order_view, name='delete_sales_order'),
    path('sales_order/<str:pk>/print',print_sales_order_view, name='print_sales_order'),

    path('upload/<data>/',uploadCSV, name='upload'),
    path('admin/', admin.site.urls),

    # Route for history
    path('history/', display_history_view, name='history'),

