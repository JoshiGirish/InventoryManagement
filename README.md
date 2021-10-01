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
				<code>/company</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/company_views/index.html#InvManage.views.company_views.create_company_view" style="font-style:italic;">create_company_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/companies</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/company_views/index.html#InvManage.views.company_views.display_companies_view" style="font-style:italic;">display_companies_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/company/update</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/company_views/index.html#InvManage.views.company_views.update_company_view" style="font-style:italic;">update_company_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/company/&lt;str:pk&gt;/delete</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/company_views/index.html#InvManage.views.company_views.delete_company_view" style="font-style:italic;">delete_company_view(request, pk)</a>
			</td>
		</tr>
		<!-- Product APIs -->
		<tr>
			<td rowspan="5">
				Product
			</td>
			<td>
				<code>/product</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/product_views/index.html#InvManage.views.product_views.create_product_view" style="font-style:italic;">create_product_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/products</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/product_views/index.html#InvManage.views.product_views.display_products_view" style="font-style:italic;">display_products_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/product/update</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/product_views/index.html#InvManage.views.product_views.update_product_view" style="font-style:italic;">update_product_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/product/&lt;str:pk&gt;/delete</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/product_views/index.html#InvManage.views.product_views.delete_product_view" style="font-style:italic;">delete_product_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/upload/&lt;data&gt;</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/product_views/index.html#InvManage.views.product_views.uploadCSV" style="font-style:italic;">uploadCSV(request, data)</a>
			</td>
		</tr>
		<!-- Vendor APIs -->
		<tr>
			<td rowspan="5">
				Vendor
			</td>
			<td>
				<code>/vendor</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/vendor_views/index.html#InvManage.views.vendor_views.create_vendor_view" style="font-style:italic;">create_vendor_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/vendors</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/vendor_views/index.html#InvManage.views.vendor_views.display_vendors_view" style="font-style:italic;">display_vendors_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/vendor/update</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/vendor_views/index.html#InvManage.views.vendor_views.update_vendor_view" style="font-style:italic;">update_vendor_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/vendor/&lt;str:pk&gt;/delete</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/vendor_views/index.html#InvManage.views.vendor_views.delete_vendor_view" style="font-style:italic;">delete_vendor_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/get_vendor</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/vendor_views/index.html#InvManage.views.vendor_views.get_vendor" style="font-style:italic;">get_vendor(request)</a>
			</td>
		</tr>
		<!-- Consumer APIs -->
		<tr>
			<td rowspan="5">
				Consumer
			</td>
			<td>
				<code>/consumer</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/consumer_views/index.html#InvManage.views.consumer_views.create_consumer_view" style="font-style:italic;">create_consumer_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/consumers</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/consumer_views/index.html#InvManage.views.consumer_views.display_consumers_view" style="font-style:italic;">display_consumers_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/consumer/update</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/consumer_views/index.html#InvManage.views.consumer_views.update_consumer_view" style="font-style:italic;">update_consumer_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/consumer/&lt;str:pk&gt;/delete</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/consumer_views/index.html#InvManage.views.consumer_views.delete_consumer_view" style="font-style:italic;">delete_consumer_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/get_consumer</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/consumer_views/index.html#InvManage.views.consumer_views.get_consumer" style="font-style:italic;">get_consumer(request)</a>
			</td>
		</tr>
		<!-- GRN APIs -->
		<tr>
			<td rowspan="5">
				GoodsReceiptNote
			</td>
			<td>
				<code>/grn</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/goods_receipt_note_views/index.html#InvManage.views.goods_receipt_note_views.create_grn_view" style="font-style:italic;">create_grn_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/grns</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/goods_receipt_note_views/index.html#InvManage.views.goods_receipt_note_views.display_grns_view" style="font-style:italic;">display_grns_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/grn/update</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/goods_receipt_note_views/index.html#InvManage.views.goods_receipt_note_views.update_grn_view" style="font-style:italic;">update_grn_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/grn/&lt;str:pk&gt;/delete</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/goods_receipt_note_views/index.html#InvManage.views.goods_receipt_note_views.delete_grn_view" style="font-style:italic;">delete_grn_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/grn/&lt;str:pk&gt;/print</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/goods_receipt_note_views/index.html#InvManage.views.goods_receipt_note_views.print_grn_view" style="font-style:italic;">print_grn_view(request, pk)</a>
			</td>
		</tr>
		<!-- PO APIs -->
		<tr>
			<td rowspan="6">
				PurchaseOrder
			</td>
			<td>
				<code>/purchase_order</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.create_purchase_order_view" style="font-style:italic;">create_purchase_order_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/purchase_orders</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.display_purchase_orders_view" style="font-style:italic;">display_purchase_orders_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/purchase_order/update</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.update_purchase_order_view" style="font-style:italic;">update_purchase_order_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/purchase_order/&lt;str:pk&gt;/delete</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.delete_purchase_order_view" style="font-style:italic;">delete_purchase_order_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/purchase_order/&lt;str:pk&gt;/print</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.print_purchase_order_view" style="font-style:italic;">print_purchase_order_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/product_purchase_entries</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/purchase_order_views/index.html#InvManage.views.purchase_order_views.get_product_purchase_entries_view" style="font-style:italic;">get_product_purchase_entries_view(request)</a>
			</td>
		</tr>
		<!-- SO APIs -->
		<tr>
			<td rowspan="6">
				SalesOrder
			</td>
			<td>
				<code>/sales_order</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/sales_order_views/index.html#InvManage.views.sales_order_views.create_sales_order_view" style="font-style:italic;">create_sales_order_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/sales_orders</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/sales_order_views/index.html#InvManage.views.sales_order_views.display_sales_orders_view" style="font-style:italic;">display_sales_orders_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/sales_order/update</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/sales_order_views/index.html#InvManage.views.sales_order_views.update_sales_order_view" style="font-style:italic;">update_sales_order_view(request)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/sales_order/&lt;str:pk&gt;/delete</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/sales_order_views/index.html#InvManage.views.sales_order_views.delete_sales_order_view" style="font-style:italic;">delete_sales_order_view(request, pk)</a>
			</td>
		</tr>
		<tr>
			<td>
				<code>/sales_order/&lt;str:pk&gt;/print</code>
			</td>
			<td>
				<a href="https://inventory-management.readthedocs.io/en/latest/autoapi/InvManage/views/sales_order_views/index.html#InvManage.views.sales_order_views.print_sales_order_view" style="font-style:italic;">print_sales_order_view(request, pk)</a>
			</td>
		</tr>
	</tbody>
</table>

## Resources

- Introduction : [About INVENT](https://inventory-management.readthedocs.io/en/latest/about.html)

- Quick Start Tutorials : [INVENT - YouTube Tutorials](https://inventory-management.readthedocs.io/en/latest/tutorials.html)

- Documentation : [INVENT v1.0.0 Documentation](https://inventory-management.readthedocs.io/en/latest/index.html)

- APIs : [INVENT API Reference](https://inventory-management.readthedocs.io/en/latest/autoapi/index.html)

