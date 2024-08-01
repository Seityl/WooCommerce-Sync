// Copyright (c) 2024, Jeriel Francis and contributors
// For license information, please see license.txt

frappe.ui.form.on("WooCommerce Sync", {
	refresh: function(frm) {
        frm.add_custom_button(__('Sync Items'), function(){
            frappe.call({
                method:"woo_sync.woo_requests.get_request"
            })
        });
	}
});
