# INVENT

[![INVENT](https://img.shields.io/badge/INVENT-python-blue)](#)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/JoshiGirish/InventoryManagement)](https://github.com/JoshiGirish/InventoryManagement/releases/tag/v1.0.0)
[![GitHub issues](https://img.shields.io/github/issues-raw/JoshiGirish/InventoryManagement?color=red)](https://github.com/JoshiGirish/InventoryManagement/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/JoshiGirish/InventoryManagement?color=green)](https://github.com/JoshiGirish/InventoryManagement/issues?q=is%3Aissue+is%3Aclosed)


**INVENT** is an inventory management software. It is a minimalistic demo application based on `Django` web framework. It was created to demostrate the rapid prototyping capabililties of `Django` for web application development.

![INVENT](/docs/images/main.png)


## REST API

For REST API documentation check out the `InvManage.views` section.

<table style="border:1px solid dimgray;">
	<thead>
		<tr>
			<th>
				Model
			</th>
			<th>
				API Endpoint
			</th>
			<th>
				View
			</th>
		</tr>
	</thead>
	<tbody>
	<!-- Company APIs -->
		<tr>
			<td rowspan="4">
				Company
			</td>
			<td>
				`'/company'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/company_views/index.html#InvManage.views.company_views.create_company_view">create_company_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/companies`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/company_views/index.html#InvManage.views.company_views.display_companies_view">display_companies_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/company/update'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/company_views/index.html#InvManage.views.company_views.update_company_view">update_company_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/company/&lt;str:pk&gt;/delete'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/company_views/index.html#InvManage.views.company_views.delete_company_view">delete_company_view(request, pk)</a>
			</td>
		</tr>
		<!-- Product APIs -->
		<tr>
			<td rowspan="5">
				Product
			</td>
			<td>
				`'/product'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/product_views/index.html#InvManage.views.product_views.create_product_view">create_product_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/products`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/product_views/index.html#InvManage.views.product_views.display_products_view">display_products_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/product/update'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/product_views/index.html#InvManage.views.product_views.update_product_view">update_product_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/product/&lt;str:pk&gt;/delete'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/product_views/index.html#InvManage.views.product_views.delete_product_view">delete_product_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/upload/&lt;data&gt;'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/product_views/index.html#InvManage.views.product_views.uploadCSV">uploadCSV(request, data)</a>
			</td>
		</tr>
		<!-- Vendor APIs -->
		<tr>
			<td rowspan="5">
				Vendor
			</td>
			<td>
				`'/vendor'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/vendor_views/index.html#InvManage.views.vendor_views.create_vendor_view">create_vendor_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/vendors`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/vendor_views/index.html#InvManage.views.vendor_views.display_vendors_view">display_vendors_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/vendor/update'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/vendor_views/index.html#InvManage.views.vendor_views.update_vendor_view">update_vendor_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/vendor/&lt;str:pk&gt;/delete'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/vendor_views/index.html#InvManage.views.vendor_views.delete_vendor_view">delete_vendor_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/get_vendor'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/vendor_views/index.html#InvManage.views.vendor_views.get_vendor">get_vendor(request)</a>
			</td>
		</tr>
		<!-- Consumer APIs -->
		<tr>
			<td rowspan="5">
				Consumer
			</td>
			<td>
				`'/consumer'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/consumer_views/index.html#InvManage.views.consumer_views.create_consumer_view">create_consumer_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/consumers`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/consumer_views/index.html#InvManage.views.consumer_views.display_consumers_view">display_consumers_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/consumer/update'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/consumer_views/index.html#InvManage.views.consumer_views.update_consumer_view">update_consumer_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/consumer/&lt;str:pk&gt;/delete'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/consumer_views/index.html#InvManage.views.consumer_views.delete_consumer_view">delete_consumer_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/get_consumer'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/consumer_views/index.html#InvManage.views.consumer_views.get_consumer">get_consumer(request)</a>
			</td>
		</tr>
		<!-- GRN APIs -->
		<tr>
			<td rowspan="5">
				GoodsReceiptNote
			</td>
			<td>
				`'/grn'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/goods_receipt_note_views/index.html#InvManage.views.goods_receipt_note_views.create_grn_view">create_grn_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/grns`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/goods_receipt_note_views/index.html#InvManage.views.goods_receipt_note_views.display_grns_view">display_grns_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/grn/update'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/goods_receipt_note_views/index.html#InvManage.views.goods_receipt_note_views.update_grn_view">update_grn_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/grn/&lt;str:pk&gt;/delete'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/goods_receipt_note_views/index.html#InvManage.views.goods_receipt_note_views.delete_grn_view">delete_grn_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/grn/&lt;str:pk&gt;/print'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/goods_receipt_note_views/index.html#InvManage.views.goods_receipt_note_views.print_grn_view">print_grn_view(request, pk)</a>
			</td>
		</tr>
		<!-- PO APIs -->
		<tr>
			<td rowspan="6">
				PurchaseOrder
			</td>
			<td>
				`'/purchase_order'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.create_purchase_order_view">create_purchase_order_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/purchase_orders`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.display_purchase_orders_view">display_purchase_orders_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/purchase_order/update'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.update_purchase_order_view">update_purchase_order_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/purchase_order/&lt;str:pk&gt;/delete'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.delete_purchase_order_view">delete_purchase_order_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/purchase_order/&lt;str:pk&gt;/print'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.print_purchase_order_view">print_purchase_order_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/product_purchase_entries'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.get_product_purchase_entries_view">get_product_purchase_entries_view(request)</a>
			</td>
		</tr>
		<!-- SO APIs -->
		<tr>
			<td rowspan="6">
				SalesOrder
			</td>
			<td>
				`'/sales_order'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/sales_order_views/index.html#InvManage.views.sales_order_views.create_sales_order_view">create_sales_order_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/sales_orders`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/sales_order_views/index.html#InvManage.views.sales_order_views.display_sales_orders_view">display_sales_orders_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/sales_order/update'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/sales_order_views/index.html#InvManage.views.sales_order_views.update_sales_order_view">update_sales_order_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/sales_order/&lt;str:pk&gt;/delete'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/sales_order_views/index.html#InvManage.views.sales_order_views.delete_sales_order_view">delete_sales_order_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				`'/sales_order/&lt;str:pk&gt;/print'`
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/sales_order_views/index.html#InvManage.views.sales_order_views.print_sales_order_view">print_sales_order_view(request, pk)</a>
			</td>
		</tr>
	</tbody>
</table>

## Resources

- Introduction : [About INVENT](https://inventory-management.readthedocs.io/en/latest/about.html)

- Quick Start Tutorials : [INVENT - YouTube Tutorials](https://inventory-management.readthedocs.io/en/latest/tutorials.html)

- Documentation : [INVENT v1.0.0 Documentation](https://inventory-management.readthedocs.io/en/latest/index.html)

- APIs : [INVENT API Reference](https://inventory-management.readthedocs.io/en/latest/autoapi/index.html)

