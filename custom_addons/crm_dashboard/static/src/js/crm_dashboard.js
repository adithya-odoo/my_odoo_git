/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from  "@odoo/owl";
const actionRegistry = registry.category("actions");
class CrmDashboard extends Component {
   setup() {
         super.setup()
         this.orm = useService('orm')
         this._crm_data()
   }
   async _crm_data(){
    var self = this;
    await this.orm.call("crm.lead", "get_tiles_data", [], {}).then(function(result){
            $('#my_lead').append('<span>' + result.total_leads + '</span>');
            $('#my_opportunity').append('<span>' + result.total_opportunity + '</span>');
            $('#revenue').append('<span>' + result.currency + result.expected_revenue + '</span>');
            $('#won').append('<span>' +result.won + '</span>');
            $('#lost').append('<span>' +result.lost + '</span>');
            });
        };
}
CrmDashboard.template = "crm_dashboard.CrmDashboard";
//  Tag name that we entered in the first step.
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
