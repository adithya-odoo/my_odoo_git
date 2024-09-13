/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";

export function _chunk(array, size) {
    console.log(array, size, "fffff")
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
            var refEl = this.$el.find("#repair_order_carousel")
            console.log("first")
            console.log(this)
            const { repair_orders} = this
            console.log(repair_orders,"23456")
            var chunkData = _chunk(repair_orders, 4)
            chunkData[0].is_active = true
            console.log(unique_id)
            const randomId = function(length = 6) {
              return Math.random().toString(36).substring(2, length+2);
               };
            var unique_id = String(randomId());
            console.log(typeof unique_id)
              console.log(chunkData,"chunkData")
            refEl.html(renderToElement('vehicle_management.repair_order_wise', {
                chunkData,
                unique_id
            }))
        }

});
PublicWidget.registry.repair_order_snippet = DynamicSnippet;
return DynamicSnippet;
