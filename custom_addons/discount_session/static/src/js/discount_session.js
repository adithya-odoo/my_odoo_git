/** @odoo-module */
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { Order,  Orderline } from "@point_of_sale/app/store/models";

patch(Order.prototype, {
async pay() {
   if((this.pos.config.discount_limit && this.get_total_discount()) || (this.pos.config.discount_limit_percentage && this.get_total_discount())){
       if(this.pos.config.type == 'amount'){
            var total_discount_pos = await this.env.services.orm.call('pos.order','return_total_discount_pos',
                                                   [this.pos_session_id])
            var set_discount_limit = this.pos.config.discount_limit
            console.log(this.pos.config)
             console.log(this.pos.config.type)
             if (this.get_total_discount() > set_discount_limit || (total_discount_pos+this.get_total_discount()) > set_discount_limit){
                   this.env.services.popup.add(ErrorPopup, {
                    title: _t("Alert"),
                    body: _t('Discount limit for the current session is exceeded'),
                  });
             }
             else {
                  return {
                     ...super.pay(...arguments),
                         };
                  }
       }
       else if(this.pos.config.type == 'percentage'){
         var set_discount_limit = this.pos.config.discount_limit_percentage * 100
         var order_lines = this.orderlines;
         console.log(this)
         var total_without_discount = 0;
         for(let i=0; i < order_lines.length; i++ ){

           total_without_discount += order_lines[i].get_price_with_tax_before_discount()
         }
            console.log(total_without_discount)
            console.log(this.get_total_discount())
            console.log(this.pos.config.discount_limit_percentage)

          var total_discount_percentage = (this.get_total_discount() / total_without_discount)*100
          console.log(total_discount_percentage)
          if(set_discount_limit < total_discount_percentage){
            this.env.services.popup.add(ErrorPopup, {
                    title: _t("Alert"),
                    body: _t('Your Discount limit percentage is only '+ set_discount_limit + '% but the current order discount is '+total_discount_percentage.toFixed(2)+'%'),
                  });
          }

          else{
          return {
                  ...super.pay(...arguments),
                  };
         }

       }

   else {
       return {
           ...super.pay(...arguments),
        };
       }
   }
   }
});



