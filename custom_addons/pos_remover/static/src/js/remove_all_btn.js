/** @odoo-module */
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";

export class DeleteOrderLine extends Component{
    static template = "clearAllButton";
    async onClick(){
    var order = this.env.services.pos.get_order();
    var lines = order.get_orderlines()
    lines.filter(line => line.get_product()).forEach(line => order.removeOrderline(line))
   }
 }
ProductScreen.addControlButton({
component : DeleteOrderLine
})