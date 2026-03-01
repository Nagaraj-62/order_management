// // Copyright (c) 2026, nagaraju and contributors
// // For license information, please see license.txt

// const { useCallback } = require("react");

frappe.ui.form.on("Sales Order", {
    refresh(frm) {
        if (frm.doc.status === "Draft") {
            frm.add_custom_button("Mark Confirmed", function () {
                frm.set_value("status", "Confirmed");
                frm.save();
            });
        }
    }
});


frappe.ui.form.on("Sales Order Item", {
    quantity(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (row.item && row.quantity) {
            console.log(`Fetching stock for item: ${row.item}`);
            //  Fetch stock from Item Doctype
            frappe.call({
                method: "frappe.client.get_value",
                args: {
                    doctype: "Item",
                    filters: { item_name: row.item },
                    fieldname: ["stock", "price"]
                },
                callback: function (r) {
                    if (r.message) {
                        console.log(r.message);
                        let stock = r.message.stock;
                        let price = r.message.price;

                        // Set rate From item master 
                        frm.set_value("items", frm.doc.items);

                        row.rate = price;
                        row.amount = row.quantity * row.rate;

                        // Show warning if quantity > stock

                        if (row.quantity > stock) {
                            frappe.msgprint({
                                title: "Stock Warning",
                                message: `Only ${stock} items available in stock. for item ${row.item}`,
                                indicator: "orange"
                            });
                        }

                        frm.refresh_field("items");
                        calculate_total(frm);
                    }
                }
            });
        }
    },

    rate(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        row.amount = (row.quantity || 0) * (row.rate || 0);
        frm.refresh_field("items");
        calculate_total(frm);
    }
});


function calculate_total(frm) {
    let total = 0;

    frm.doc.items.forEach(row => {
        total += row.amount || 0;
    });

    frm.set_value("total_amount", total);
}