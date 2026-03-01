import frappe
from frappe.utils import getdate

@frappe.whitelist()
def get_orders(from_date=None, to_date=None):
    try:
        filters = {"status": "Confirmed"}

        if from_date and to_date:
            filters["order_date"] = ["between", [from_date, to_date]]

        orders = frappe.get_all(
            "Sales Order",
            filters=filters,
            fields=["name", "customer", "order_date", "total_amount"]
        )

        for order in orders:
            order["items"] = frappe.get_all(
                "Sales Order Item",
                filters={"parent": order.name},
                fields=["item", "quantity", "rate", "amount"]
            )

        return {"status": "success", "data": orders}

    except Exception as e:
        frappe.log_error(frappe.get_traceback())
        return {"status": "error", "message": str(e)}