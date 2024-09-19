/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
patch(PosStore.prototype, {
   getReceiptHeaderData() {
   (this.get_order().orderlines).forEach((el) => console.log(el.product.product_owner_id[1]))
       return {
           ...super.getReceiptHeaderData(...arguments),
           owner: this.get_order().orderlines
       };
   },
});
