import json
import frappe
import requests
from frappe import _
from erpnext.stock.utils import get_bin
from .exceptions import woocommerceError
from frappe.utils import get_datetime, cint
from .utils import make_woocommerce_log, disable_woocommerce_sync_for_item
from .woo_requests import get_woocommerce_settings, get_request, post_request, put_request
from .item_sync import sync_item_by_item_code, get_item_codes_from_woocommerce

@frappe.whitelist()
def bulk_sync_items_to_woocommerce():
    get_item_codes_from_woocommerce()

# TODO: Finish this
@frappe.whitelist()
def sync_single_item_to_woocommerce():
    woocommerce_settings = get_woocommerce_settings()
    sync_based_on = woocommerce_settings["sync_based_on"] 

    # make_woocommerce_log(title="Sync Based On", status="Success", method="sync_single_item_to_woocommerce", message=sync_based_on)
    
    # if (sync_based_on == "WooCommerce Item ID"):
        # sync_item_by_woocommerce_id()

    if (sync_based_on == "Item Code"):
        sync_item_by_item_code()