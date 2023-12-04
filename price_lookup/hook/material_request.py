import frappe

@frappe.whitelist()
def get_inventory(item_code = None):
    inventory_details = frappe.db.sql("""
        select 
            warehouse, actual_qty, ordered_qty
        from 
            `tabBin` 
        where 
            item_code = '{0}';""".format(item_code), as_dict = True)

    return inventory_details