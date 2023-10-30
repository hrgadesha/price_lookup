import frappe
from frappe.utils import flt, cint

@frappe.whitelist()
def get_price_history(item_code = None, history_based_on = None, party = None):
    record_limit = cint(frappe.db.get_single_value('Price Lookup Settings', 'quotation_historical_data_limit')) or 3

    conditions = " and qtn_item.item_code = '{0}'".format(item_code)

    if history_based_on == "Selected Party":
        conditions += " and qtn.party_name = '{0}'".format(party)

    quote_item_details = frappe.db.sql("""
        select 
            qtn.name as quotation_id, 
            qtn.quotation_to as party_type, 
            qtn.party_name as party_name, 
            qtn.transaction_date as date, 
            qtn_item.item_code as item_code, 
            qtn_item.item_name as item_name, 
            qtn_item.price_list_rate as mrp, 
            qtn_item.discount_amount as discount_amount,
            qtn_item.discount_percentage as discount_percent,
            qtn_item.rate as rate 
        from 
            `tabQuotation` qtn, `tabQuotation Item` qtn_item 
        where 
            qtn.name = qtn_item.parent and qtn.docstatus = 1 and 
            qtn.status not in ('Expired', 'Lost') {0}
        order by 
            qtn.name desc
        limit {1};""".format(conditions, record_limit), as_dict = True)

    return quote_item_details