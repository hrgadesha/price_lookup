import frappe
from frappe.utils import flt, cint

@frappe.whitelist()
def get_price_history(item_code = None, history_based_on = None, party = None):
    record_limit = cint(frappe.db.get_single_value('Price Lookup Settings', 'sales_order_historical_data_limit')) or 3

    conditions = " and so_item.item_code = '{0}'".format(item_code)

    if history_based_on == "Selected Party":
        conditions += " and so.customer = '{0}'".format(party)

    quote_item_details = frappe.db.sql("""
        select 
            so.name as so_id, 
            so.customer as customer, 
            so.transaction_date as date, 
            so_item.item_code as item_code, 
            so_item.item_name as item_name, 
            so_item.price_list_rate as mrp, 
            so_item.discount_amount as discount_amount,
            so_item.discount_percentage as discount_percent,
            so_item.rate as rate 
        from 
            `tabSales Order` so, `tabSales Order Item` so_item 
        where 
            so.name = so_item.parent and so.docstatus = 1 {0}
        order by 
            so.name desc
        limit {1};""".format(conditions, record_limit), as_dict = True)

    return quote_item_details