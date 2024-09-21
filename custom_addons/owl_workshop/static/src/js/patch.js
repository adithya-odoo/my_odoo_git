/**@odoo-module*/
import { InputBox } from "./input_box"
import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import { useEffect } from "@odoo/owl";
import { useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

patch(InputBox.prototype, {
    setup() {
       this.orm = useService("orm");
       this.action = useService("action");
       this.uniqueBoxId = useRef("uniqueInputBox")
        super.setup()
        this.state = useState(
        {
        value: 0,
        }
        )

 useEffect(
    () => { this.demo()
            console.log("inside the useEffect")}, //calling the demo if the value in this.state.value changes
    () =>[this.state.value])
 },
    demofu(e){
    this.state.value = this.state.value + e
    },

    newfunc(){
    console.log(this.uniqueBoxId.el.value)
//    this.uniqueBoxId.el.value = "yf"
    },

// demo function will call with the value change in this.state.value
    demo()
    {
    console.log("inside the demo function")
    },

   //orm service
    async fetchsaleorder(){
         this.state.orders = await this.orm.call("demo.demo", "fetch_sales", []);
         var searchOrder = await this.orm.search("sale.order",[], {limit:10})
         var searchReadOrder = await this.orm.searchRead("sale.order",[],[], {limit:10})
         console.log(searchOrder, "search")
         console.log(searchReadOrder, "Search Read")
         console.log(this.state.orders, "with Model")

    },

     //actionservice
     opensaleorder(){
     this.action.doAction({
        type: 'ir.actions.act_window',
        res_model: 'sale.order',
        res_id: 41,
        views: [[false, "form"]],
        view_mode: "form",
        target: "current",

     })
     }


});