/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";

export function _chunk(array, size) {
    var result = [];
    for (let i = 0; i < array.length; i += size) {
             result.push(array.slice(i, i + size));
    }
    return result;
    }

var DynamicSnippet = PublicWidget.Widget.extend({
selector: '.repair_order_snippet',

willStart: async function () {
            const data = await jsonrpc('/repair-snippet', {})
            const repair_orders = data
            Object.assign(this, {
                repair_orders
            })
        },
          start: function () {
            var refEl = this.$el.find("#repair_order_carousel")
            const { repair_orders} = this
            var chunkData = _chunk(repair_orders, 4)
            chunkData[0].is_active = true
            const randomId = function(length = 6) {
              return Math.random().toString(36).substring(2, length+2);
               };
            var unique_id = String(randomId());
            refEl.html(renderToElement('vehicle_management.repair_order_wise', {
                chunkData,
                unique_id
            }))
        }

});
PublicWidget.registry.repair_order_snippet = DynamicSnippet;
return DynamicSnippet;
