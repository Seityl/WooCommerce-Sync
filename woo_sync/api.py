import json
import frappe
import requests
from frappe import _
from erpnext.stock.utils import get_bin
from .exceptions import woocommerceError
from frappe.utils import get_datetime, cint
from .utils import make_woocommerce_log, disable_woocommerce_sync_for_item
from .woo_requests import get_request, post_request, put_request

# FOR TESTING 

item = frappe.get_doc("Item", "JP24680")

# FOR TESTING
@frappe.whitelist()
def sync_item_to_woocommerce():
    # woocommerce_settings = frappe.get_doc("WooCommerce Sync", "WooCommerce Sync")
    # item_id = woocommerce_settings.woocommerce_item_id
    # path = 'wp-json/wc/v3/products/{0}'.format(item_id)
    # data = {
    #     "stock_quantity": 12
    # }
    # post_request(path, data)
    # path = 'wp-json/wc/v3/products?sku=JP24680'
    # woocommerce_item_id = get_request(path)
    # make_woocommerce_log(title="SUCCESS: GET", status="Success", method="get_request", message=woocommerce_item_id[0]['id'], request_data='N/A', exception=True)

    update_item_stock_qty()

@frappe.whitelist()
def get_product_update_dict_and_resource(woocommerce_product_id, actual_qty=0):
    item_data = {}
    item_data["stock_quantity"] = "{0}".format(cint(actual_qty))
    item_data["manage_stock"] = "1"

    resource = "products/{0}".format(woocommerce_product_id)

    return item_data, resource

@frappe.whitelist()
def get_woocommerce_item_id(item_code='JP23575'):
    path = 'wp-json/wc/v3/products?sku={0}'.format(item_code)
    r = get_request(path)
    woocommerce_item_id = r[0]['id']

    return woocommerce_item_id

@frappe.whitelist()
def update_item_stock_qty(item_code='JP23575'):
    woocommerce_settings = frappe.get_doc("WooCommerce Sync", "WooCommerce Sync")

    try:
        # FOR TESTING // JP24680 -> item.item_code
        update_item_stock(item_code, woocommerce_settings)
    except woocommerceError as e:
        make_woocommerce_log(title="{0}".format(e), status="Error", method="sync_woocommerce_items", message=frappe.get_traceback(),
            request_data=item, exception=True)

    except Exception as e:
        if e.args[0] and e.args[0].startswith("402"):
            raise e
        else:
            make_woocommerce_log(title="{0}".format(e), status="Error", method="sync_woocommerce_items", message=frappe.get_traceback(),
                request_data=item, exception=True)

@frappe.whitelist()
def update_item_stock(item_code, woocommerce_settings):
    item = frappe.get_doc("Item", item_code)

    bin = get_bin(item_code, woocommerce_settings.warehouse)

    actual_qty = bin.actual_qty
    reserved_qty = bin.reserved_qty
    qty = actual_qty - reserved_qty

    item_data, resource = get_product_update_dict_and_resource(get_woocommerce_item_id(), actual_qty=qty)
    try:
        #make_woocommerce_log(title="Update stock of {0}".format(item.barcode), status="Started", method="update_item_stock", message="Resource: {0}, data: {1}".format(resource, item_data))
        put_request(resource, item_data)
    except requests.exceptions.HTTPError as e:
        if e.args[0] and e.args[0].startswith("404"):
            make_woocommerce_log(title=e.message, status="Error", method="update_item_stock", message=frappe.get_traceback(),
                request_data=item_data, exception=True)
            disable_woocommerce_sync_for_item(item)
        else:
            raise e