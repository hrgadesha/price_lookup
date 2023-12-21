import frappe
from frappe.utils import flt, cint

@frappe.whitelist()
def get_price_history(item_code = None, history_based_on = None, party = None):
    record_limit = cint(frappe.db.get_single_value('Price Lookup Settings', 'purchase_order_historical_data_limit')) or 3

    conditions = " and po_item.item_code = '{0}'".format(item_code)

    if history_based_on == "Selected Party":
        conditions += " and po.supplier = '{0}'".format(party)

    po_item_details = frappe.db.sql("""
        select 
            po.name as po_id, 
            po.supplier as supplier, 
            po.transaction_date as date, 
            po_item.item_code as item_code, 
            po_item.item_name as item_name, 
            po_item.price_list_rate as mrp, 
            po_item.discount_amount as discount_amount,
            po_item.discount_percentage as discount_percent,
            po_item.rate as rate 
        from 
            `tabPurchase Order` po, `tabPurchase Order Item` po_item 
        where 
            po.name = po_item.parent and po.docstatus = 1 {0}
        order by 
            po.name desc
        limit {1};""".format(conditions, record_limit), as_dict = True)

    return po_item_details