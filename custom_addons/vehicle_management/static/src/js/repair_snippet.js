/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";

export function chunk(array, size) {
    console.log(array)
    console.log(array.length, "hell")
    var result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
    }
var DynamicSnippet = PublicWidget.Widget.extend({
selector: '.repair_order_snippet',
willStart: async function () {
            console.log("willStart")
            const data = await jsonrpc('/repair-snippet', {})
            const repair_orders = data
            console.log(repair_orders, 'kozhapam')
            Object.assign(this, {
                repair_orders
            })
        },
          start: function () {
            const refEl = this.$el.find("#repair_order_carousel")
            console.log("first")
            console.log(this)
            const { repair_orders} = this
            console.log(repair_orders,"23456")
            const chunkData = chunk(repair_orders, 4)
            console.log(chunkData,"chunkData")
            refEl.html(renderToElement('vehicle_management.repair_order_wise', {
                repair_orders,
                chunkData
            }))
        }
});
PublicWidget.registry.repair_order_snippet = DynamicSnippet;
return DynamicSnippet;
