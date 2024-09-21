/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
patch(Order.prototype, {

  async pay() {
    console.log(this.pos_session_id)
    console.log(this.pos.config.discount_limit)
    return super.pay(...arguments);
    }
});
