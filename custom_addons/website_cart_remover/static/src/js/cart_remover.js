/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";

console.log('haiiii')
publicWidget.registry.cartRemover = publicWidget.Widget.extend({
     selector:'.oe_cart',
     events: {
        'click .remove_cart_item' : '_onRemoveBtnClick',
    },

    _onRemoveBtnClick:function(ev){
    ev.preventDefault()
     var newone = $('.o_cart_product').find('.js_quantity').val(0)
     console.log(ev)
//       newone.trigger('change');

    }

});
