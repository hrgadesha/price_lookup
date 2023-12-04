frappe.ui.form.on("Material Request Item", {
    item_code(frm, cdt, cdn) {
        let child_row = locals[cdt][cdn];
        if (child_row.item_code && frm.doc.material_request_type == "Purchase") {
            set_inventory_details(frm, child_row);
        }
    },
    sync_updated_data(frm, cdt, cdn) {
        let child_row = locals[cdt][cdn];
        if (child_row.item_code && frm.doc.material_request_type == "Purchase") {
            set_inventory_details(frm, child_row);
        }
    }
});

function set_inventory_details(frm, child_row) {
    frappe.call({
        method: 'price_lookup.hook.material_request.get_inventory',
        args: {
            item_code: child_row.item_code,
        },
        callback: function (r) {
            if (r.message.length == 0) {
                frappe.model.set_value(child_row.doctype, child_row.name,
                    'stock_details', `<div style="text-align: center; font-weight: bold; color: red;">
                        No Inventory Found
                    </div>`
                );
            }
            else {
                let inventory_data = r.message;
                let prepared_data = `<table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Warehouse</th>
                        <th style="text-align: right;">Actual Qty</th>
                        <th style="text-align: right;">In Transit Qty</th>
                    </tr>
                </thead>
                <tbody>`
                $.each(inventory_data, function (i) {
                    prepared_data = prepared_data + `<tr>
                        <td>${inventory_data[i].warehouse}</td>
                        <td style="text-align: right;">${format_number(inventory_data[i].actual_qty)}</td>
                        <td style="text-align: right;">${format_number(inventory_data[i].ordered_qty)}</td>
                    </tr>`
                })
                prepared_data = prepared_data + `</tbody></table>`;
                frappe.model.set_value(child_row.doctype, child_row.name,
                    'stock_details', prepared_data
                );
            }
        }
    });
}