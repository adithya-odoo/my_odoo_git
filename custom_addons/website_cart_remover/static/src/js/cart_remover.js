/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.cartRemover = publicWidget.Widget.extend({
     selector:'.oe_cart',
     events: {
        'click .remove_cart_item' : '_onRemoveBtnClick',
    },
      _onRemoveBtnClick: function(){
      jsonrpc("/shop/clear_cart", {}).then(function(){
            location.reload();
        });
        return false;
        }
});
