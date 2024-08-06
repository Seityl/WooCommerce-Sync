// Copyright (c) 2024, Jeriel Francis and contributors
// For license information, please see license.txt

frappe.ui.form.on("WooCommerce Sync", {
	refresh: function(frm) {

        // frm.add_custom_button(__('Sync Items to WooCommerce'), function(){
        //     frappe.call({
        //             method:"woo_sync.api.bulk_sync_items_to_woocommerce",
        //             freeze: true,
        //             freeze_message: __('Syncing...')
        //         })
        //     });

            frm.toggle_display('sync_based_on', false);
            // frm.set_value('item_code', '');
            frm.set_value('woocommerce_item_id', '');
            
            sync_based_on_visibility(frm);
            sync_based_on_options_visibility(frm);
	},

    sync_options: function(frm) {
        if (frm.doc.sync_options === '' || frm.doc.sync_options === 'Bulk Sync') {
            frm.remove_custom_button('Sync Item')
            frm.set_value('sync_based_on', '');
            // frm.set_value('item_code', '');
            frm.set_value('woocommerce_item_id', '');
            frm.toggle_display('sync_based_on', false);
        }
        sync_based_on_visibility(frm);
    }, 
    sync_based_on: function(frm) {
        sync_based_on_options_visibility(frm);
    }
});

function sync_based_on_visibility(frm) {
    if (frm.doc.sync_options === 'Single Item Sync') {
        frm.toggle_display('sync_based_on', true);
        frm.remove_custom_button('Sync Items to WooCommerce')
        
        frm.add_custom_button(__('Sync Item'), function(){
            if (frm.is_dirty()){
                if (frm.doc.woocommerce_item_id || frm.doc.item_code){
                    frappe.call({
                        method:"woo_sync.api.sync_single_item_to_woocommerce",
                        freeze: true,
                        freeze_message: __('Syncing Item...')                    
                    }).then(() => {
                        frm.save()
                        // frappe.msgprint("Successfully Synced Item.");
                        
                        // if(frm.doc.sync_based_on === 'Item Code'){
                        //     frm.set_value('item_code', '');
                        // }else if (frm.doc.sync_based_on === 'WooCommerce Item ID') {
                        //     frm.set_value('woocommerce_item_id', '');
                        // }
                    })
                } else {
                    frappe.msgprint('Error Syncing Item: Enter Item Code / WooCommerce Item ID');
                }
            } else {
                if (frm.doc.woocommerce_item_id || frm.doc.item_code){
                    frappe.call({
                        method:"woo_sync.api.sync_single_item_to_woocommerce",
                        freeze: true,
                        freeze_message: __('Syncing Item...')                            
                    }).then(() => {
                        frm.save()
                        // frappe.msgprint("Successfully Synced Item.");
                    })
                } else {
                    frappe.msgprint('Error Syncing Item: Enter Item Code / WooCommerce Item ID');
                }
            }
        });
    } else if (frm.doc.sync_options === 'Bulk Sync') {
        frm.remove_custom_button('Sync Item')

        frm.add_custom_button(__('Sync Items to WooCommerce'), function(){
            frappe.call({
                method:"woo_sync.api.bulk_sync_items_to_woocommerce",
                freeze: true,
                freeze_message: __('Syncing Items...')
            })
        });
    }
}

function sync_based_on_options_visibility(frm){
    if (frm.doc.sync_based_on === '') {
        frm.toggle_display('item_code', false);
        frm.toggle_display('woocommerce_item_id', false);
        frm.set_value('item_code', '');
        frm.set_value('woocommerce_item_id', '');

    }
    if (frm.doc.sync_based_on === 'Item Code') {
        frm.toggle_display('item_code', true);
        frm.toggle_display('woocommerce_item_id', false);
    }
    if (frm.doc.sync_based_on === 'WooCommerce Item ID') {
        frm.toggle_display('woocommerce_item_id', true);
        frm.toggle_display('item_code', false);
    }
    
}