/** @odoo-module */

// Import necessary components from Odoo Point of Sale module
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

// Patch the Orderline component to add the removeLine function
patch(Orderline.prototype, {
    removeLine() {
        // Access the current order
        const order = this.env.services.pos.get_order();

        // Find the orderline to remove based on the full product name
        const orderline = order.orderlines.find((line) => line.full_product_name == this.props.line.productName);

        // Remove the found orderline from the order
        return order.removeOrderline(orderline);
    }
});