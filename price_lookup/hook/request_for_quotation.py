import frappe
from frappe.utils import flt, cint

@frappe.whitelist()
def get_price_history(item_code = None):
    record_limit = cint(frappe.db.get_single_value('Price Lookup Settings', 'rfq_historical_data_limit')) or 3

    conditions = " and sup_qtn_item.item_code = '{0}'".format(item_code)

    sup_quote_item_details = frappe.db.sql("""
        select 
            sup_qtn.name as sup_quotation_id, 
            sup_qtn.supplier as supplier, 
            sup_qtn.transaction_date as date, 
            sup_qtn_item.item_code as item_code, 
            sup_qtn_item.item_name as item_name, 
            sup_qtn_item.price_list_rate as mrp, 
            sup_qtn_item.discount_amount as discount_amount,
            sup_qtn_item.discount_percentage as discount_percent,
            sup_qtn_item.rate as rate 
        from 
            `tabSupplier Quotation` sup_qtn, `tabSupplier Quotation Item` sup_qtn_item 
        where 
            sup_qtn.name = sup_qtn_item.parent and sup_qtn.docstatus = 1 and 
            sup_qtn.status not in ('Expired', 'Stopped') {0}
        order by 
            sup_qtn.name desc
        limit {1};""".format(conditions, record_limit), as_dict = True)

    return sup_quote_item_details