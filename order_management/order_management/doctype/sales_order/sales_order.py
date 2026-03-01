# Copyright (c) 2026, nagaraju and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SalesOrder(Document):
    def validate(self):
        if not self.items:
            frappe.throw("Please add at least one item to the sales order.")

        if self.items:
            self.total_amount=0
            for item in self.items:
                if not item.item:
                    frappe.throw(f"Item is required for row {item.idx} in the sales order items.")
                else:
                    item_doc=frappe.get_doc("Item",item.item)
                if item.quantity> item_doc.stock:
                    frappe.throw(f"Ordered Quantity {item.quantity} for item {item.item} is Greater than Available Stock {item_doc.stock}")
                
                if not item.rate:
                    item.rate=item_doc.price
                item.amount=item.quantity*item.rate
                self.total_amount+=item.amount

    def on_submit(self):
        for item in self.items:
            item_doc=frappe.get_doc("Item",item.item)
            item_doc.stock-=item.quantity
            item_doc.save()
        if self.status== "Confirmed":
            self.enqueue_email()
        frappe.logger().info(f"Order confirmed: {self.name}")

    def enqueue_email(self):
        frappe.enqueue(
            "order_management.tasks.send_email",
            order=self.name
        )