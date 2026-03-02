import frappe

def on_update_sales_order(doc, method):
    frappe.logger().info(f"Sales Order updated: {doc.name}")