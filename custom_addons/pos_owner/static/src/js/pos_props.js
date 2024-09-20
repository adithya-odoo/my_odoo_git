/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/store/models";
patch(Orderline.prototype, {
    getDisplayData() {
    return {
            ...super.getDisplayData(),
             owner: this.get_product().product_owner_id
       };
    }
});

