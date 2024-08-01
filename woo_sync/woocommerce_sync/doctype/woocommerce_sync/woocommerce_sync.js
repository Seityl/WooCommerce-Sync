// Copyright (c) 2024, Jeriel Francis and contributors
// For license information, please see license.txt

frappe.ui.form.on("WooCommerce Sync", {
	refresh: function(frm) {
        frm.add_custom_button(__('Sync Items to WooCommerce'), function(){
            frappe.call({
                method:"woo_sync.api.sync_item_to_woocommerce"
            })
        });
        frm.add_custom_button(__('Sync Item'), function(){
            frappe.call({
                method:"woo_sync.api.sync_item_to_woocommerce"
            })
        });
	}
});
