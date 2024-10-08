/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";


publicWidget.registry.repairform = publicWidget.Widget.extend({
    selector: '.order_website_form',
    events: {
        'change select[name="vehicle_type_field"]': 'onTypeChange',
    },

    onTypeChange: function(){
    $("#vehicle_field").empty();
    console.log($("#vehicle_type_field").val())
    var vehicle_type = $("#vehicle_type_field").val()
     jsonrpc("/web/dataset/call_kw/fleet.vehicle.model/search_read", {
            model: 'fleet.vehicle.model',
            method: 'search_read',
            args: [[['category_id', '=', parseInt(vehicle_type)]]],
            kwargs: {},
        }).then(function(data) {
                console.log(data.length)
                for(let i=0; i<data.length; i++)
                {
                let optionHTML = `<option value="${data[i]['id']}">
                                                ${data[i]['name']}</option>`;
                $("#vehicle_field").append(optionHTML);
                }
        });
    }
  });