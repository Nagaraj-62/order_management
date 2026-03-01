# Copyright (c) 2026, nagaraju and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import nowdate


class TestSalesOrder(FrappeTestCase):
    def test_order_confirmation(self):
        order = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": "Chloe Morales",
            "order_date": nowdate(),
            "status": "Draft",
            "items": [{
                "item": "Cucumber",
                "quantity": 2,
                "rate": 100
            }]
        }).insert()

        order.status = "Confirmed"
        order.save()

        item = frappe.get_doc("Item", "Cucumber")

        item.stock-=2
        item.save()
