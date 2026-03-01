import frappe

def send_email(order):
    order_doc = frappe.get_doc("Sales Order", order)
    customer_doc = frappe.get_doc("Customer", order_doc.customer)

    frappe.sendmail(
        recipients=[customer_doc.email],
        subject="Order Confirmed",
        message=f"Your order {order_doc.name} has been confirmed."
    )


def daily_cancel_check():
    # Example: Auto cancel Draft orders older than 7 days
    from frappe.utils import nowdate, add_days

    cutoff_date = add_days(nowdate(), -7)

    orders = frappe.get_all(
        "Sales Order",
        filters={
            "status": "Draft",
            "order_date": ["<", cutoff_date]
        },
        pluck="name"
    )

    for order in orders:
        doc = frappe.get_doc("Sales Order", order)
        doc.status = "Cancelled"
        doc.save(ignore_permissions=True)

    frappe.logger().info("Daily cancel check executed")