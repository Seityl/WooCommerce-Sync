import frappe
import requests
from frappe import _
from .utils import make_woocommerce_log
from .exceptions import woocommerceError
from requests_oauthlib import OAuth1Session
from frappe.utils import cint

def get_woocommerce_settings():
    d = frappe.get_doc("WooCommerce Sync", "WooCommerce Sync")
    
    if d.woocommerce_url:
        d.api_secret = d.get_password(fieldname='api_secret')
        return d.as_dict()
    
    else:
        frappe.throw(_("woocommerce store URL is not configured on WooCommerce Sync"), woocommerceError)

@frappe.whitelist()
def get_request():
    settings = get_woocommerce_settings()

    woocommerce_url = settings["woocommerce_url"]
    api_key = settings["api_key"]
    api_secret = settings["api_secret"]

    woocommerce = OAuth1Session(client_key=api_key, client_secret=api_secret) 

    # Construct the API endpoint
    api_endpoint = f'{woocommerce_url}/wp-json/wc/v3/products/2295'
    
    # Make the GET request with Basic Authentication
    response = woocommerce.get(api_endpoint)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON data if successful
        r = response.json()
        frappe.throw(str(r[("id")])) 
        return response.json()
    else:
        # Handle errors or failed requests
        response.raise_for_status()  # Raises an HTTPError for bad responses