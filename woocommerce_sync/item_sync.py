import json
import frappe
import requests
from frappe import _
from erpnext.stock.utils import get_bin
from .exceptions import woocommerceError
from frappe.utils import get_datetime, cint
from .utils import make_woocommerce_log, disable_woocommerce_sync_for_item
from .woo_requests import get_woocommerce_settings, get_request, post_request, put_request

@frappe.whitelist()
def get_item_codes_from_woocommerce():
    woocommerce_settings = get_woocommerce_settings()

    item_code = 'JP25055'
    r = get_request('wp-json/wc/v3/products?sku={0}'.format(item_code))

    bin = get_bin(item_code, woocommerce_settings.warehouse)

    
    make_woocommerce_log(title="GET: Item Codes", status="Success", method="get_item_codes_from_woocommerce_products", message=bin)

# TODO: Finish this
@frappe.whitelist()
def sync_item_by_woocommerce_id(woocommerce_id):
    # update_item_stock_qty()

    # make_woocommerce_log(title="Sync With WooCommerce", status="Success", method="sync_by_woocommerce_id", message="Sync by woocommerce id")
    
    pass

@frappe.whitelist()
def sync_item_by_item_code():
    # make_woocommerce_log(title="Sync With WooCommerce", status="Success", method="sync_by_item_code", message="Sync by item code")
    
    woocommerce_settings = get_woocommerce_settings()
    item_code = woocommerce_settings['item_code']
    
    # make_woocommerce_log(title="Item Code", status="Success", method="sync_item_by_item_code", message=woocommerce_settings)

    update_item_stock_qty(item_code)

@frappe.whitelist()
def get_product_update_dict(actual_qty):
    item_data = {}
    item_data["stock_quantity"] = "{0}".format(actual_qty)
    item_data["manage_stock"] = "1"

    # make_woocommerce_log(title="Item Data", status="Success", method="get_product_update_dict", message="Item Data: {0}".format(item_data))

    return item_data

@frappe.whitelist()
def get_woocommerce_item_id(item_code):
    path = 'wp-json/wc/v3/products?sku={0}'.format(item_code)
    r = get_request(path)
    woocommerce_item_id = r[0]['id']

    # make_woocommerce_log(title="WooCommerce Item ID", status="Success", method="get_woocommerce_item_id", message="WooCommerce Item ID: {0}".format(woocommerce_item_id))

    return woocommerce_item_id

@frappe.whitelist()
def update_item_stock_qty(item_code):
    woocommerce_settings = frappe.get_doc("WooCommerce Sync", "WooCommerce Sync")

    try:
        update_item_stock(item_code, woocommerce_settings)

    except woocommerceError as e:
        make_woocommerce_log(title="{0}".format(e), status="Error", method="sync_woocommerce_items", message=frappe.get_traceback(),
            request_data=item_code, exception=True)

    except Exception as e:
        if e.args[0] and e.args[0].startswith("402"):
            raise e
            
        else:
            make_woocommerce_log(title="{0}".format(e), status="Error", method="sync_woocommerce_items", message=frappe.get_traceback(),
                request_data=item_code, exception=True)

@frappe.whitelist()
def update_item_stock(item_code, woocommerce_settings):
    item = frappe.get_doc("Item", item_code)

    bin = get_bin(item_code, woocommerce_settings.warehouse)

    actual_qty = bin.actual_qty
    reserved_qty = bin.reserved_qty
    qty = cint(actual_qty - reserved_qty)

    # make_woocommerce_log(title="Bin Data", status="Success", method="update_item_stock", message="Item Quantity: {0}".format(qty))

    woocommerce_item_id = get_woocommerce_item_id(item_code)

    resource = "wp-json/wc/v3/products/{0}".format(woocommerce_item_id)

    item_data = get_product_update_dict(qty)
    
    # make_woocommerce_log(title="Item Data", status="Success", method="get_product_update", message="Item Data: {0}".format(item_data))
    # make_woocommerce_log(title="Resource", status="Success", method="get_product_update", message="Resource: {0}".format(resource))
    
    try:
        post_request(resource, item_data)
        
    except requests.exceptions.HTTPError as e:
        if e.args[0] and e.args[0].startswith("404"):
            make_woocommerce_log(title=e.message, status="Error", method="update_item_stock", message=frappe.get_traceback(),
                request_data=item_data, exception=True)
            disable_woocommerce_sync_for_item(item)

        else:
            raise e