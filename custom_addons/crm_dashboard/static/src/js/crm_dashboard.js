/**@odoo-module **/
import { loadBundle } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
import { Component, onWillStart, useEffect, useState} from  "@odoo/owl";

const actionRegistry = registry.category("actions");
class CrmDashboard extends Component {
   setup() {
     super.setup()
     this.orm = useService('orm')
     this._crm_data()
     this.company_data()
     this.user = useService('user');
     this.state = useState({
            monthList: {},
        });

     onWillStart(async () =>{
      await loadBundle("web.chartjs_lib");
      this.isCrmManager = await this.user.hasGroup("sales_team.group_sale_manager");
      this.isCrmUser = await this.user.hasGroup("sales_team.group_sale_salesman_all_leads");
      this.isNormalUser = await this.user.hasGroup("sales_team.group_sale_salesman");
     });
     useEffect(() => {
//             this.tableChart();
             this.barChart();
             this.pieChart();
             this.doughnutChart();
             this.lineChart();
        });
   }

   async _crm_data(){
    await this.orm.call("crm.lead", "get_tiles_data", [], {}).then(function(result){
            $('#my_lead').append('<span>' + result.total_leads + '</span>');
            $('#my_opportunity').append('<span>' + result.total_opportunity + '</span>');
            $('#revenue').append('<span>' + result.currency + result.expected_revenue + '</span>');
            $('#invoiced_amount').append('<span>' + result.currency + result.invoiced_amount + '</span>');
            $('#won').append(result.won);
            $('#lost').append(result.lost);
            });
        };
    async company_data(){
    await this.orm.call("crm.lead", "get_company_data", [], {}).then(function(result){
           $('#company_details').append(result)
            });
        };

  async barChart(){
  console.log("dhv")
  await this.orm.call("crm.lead", "get_bar_data", [], {}).then(function(result){
  console.log(result.lost_leads)
  var ctx = document.getElementById('bar_canvas');
   // Create a chart
  var myChart = new Chart(ctx, {
       type: 'bar', // Choose the chart type (bar, line, pie, etc.)
       data: {
           labels: ['Lead', 'Opportunity'], // X-axis labels
           datasets: [{
               data: [result.lost_leads, result.lost_opportunity], // Y-axis data
               backgroundColor: [
                   'rgba(255, 99, 132, 0.2)',
                   'rgba(54, 162, 235, 0.2)',
                   'rgba(255, 206, 86, 0.2)'
               ],
               borderColor: [
                   'rgba(255, 99, 132, 1)',
                   'rgba(54, 162, 235, 1)',
                   'rgba(255, 206, 86, 1)'
               ],
               borderWidth: 1
           }]
       },
       options: {
           scales: {
               y: {
                   beginAtZero: true
               }
           }
       }
   });
   });
  }

  async tableChart(){
  console.log("edgvbdhbs")
  await this.orm.call("crm.lead", "get_table_data", [], {}).then(function(result){
    this.state.monthList = result
    console.log(this.state.month_list, "ftytfyt")
   });
  }

  async pieChart(){
  console.log(this)
  await this.orm.call("crm.lead", "get_pie_data", [], {}).then(function(result){
          console.log(result.name.length, result.name, result.data,  "wejdded")
           var ctx = document.getElementById('pie_canvas');
   // Create a chart
        var pieChart = new Chart(ctx, {
           type: 'pie', // Choose the chart type (bar, line, pie, etc.)
           data: {
               labels: result.name, // X-axis labels
               datasets: [{
                   data: result.data, // Y-axis data
                   backgroundColor: [
                       'rgba(255, 99, 132, 0.2)',
                       'rgba(54, 162, 235, 0.2)',
                       'rgba(255, 206, 86, 0.2)'
                   ],
                   borderColor: [
                       'rgba(255, 99, 132, 1)',
                       'rgba(54, 162, 235, 1)',
                       'rgba(255, 206, 86, 1)'
                   ],
                   borderWidth: 1
               }]
           },
           options: {
              aspectRatio: 2
           }
       });

  });
  }

  async doughnutChart(){
  console.log("cdeuygwuywhu")
  await this.orm.call("crm.lead", "get_doughnut_data", [], {}).then(function(result){
    console.log(result.name, result.data)
     var ctx = document.getElementById('doughnut_canvas');
   // Create a chart
        var doughnutChart = new Chart(ctx, {
            type: 'doughnut',
           data: {
               labels: result.name, // X-axis labels
               datasets: [{
                   data: result.data, // Y-axis data
                   backgroundColor: [
                       'rgba(255, 99, 132, 0.2)',
                       'rgba(54, 162, 235, 0.2)',
                       'rgba(255, 206, 86, 0.2)',
                       'rgba(257, 209, 76, 0.2)'
                   ],
                   borderColor: [
                       'rgba(255, 99, 132, 1)',
                       'rgba(54, 162, 235, 1)',
                       'rgba(255, 206, 86, 1)',
                       'rgba(257, 209, 76, 1)'

                   ],
                   borderWidth: 1
               }]
           },
           options: {
              aspectRatio: 2
           }
        });
     });
   }

  async lineChart(){
  await this.orm.call("crm.lead", "get_line_data", [], {}).then(function(result){
    console.log(result.name, result.data)
     var ctx = document.getElementById('line_canvas');
   // Create a chart
        var lineChart = new Chart(ctx, {
            type: 'pie',
           data: {
               labels: result.name, // X-axis labels
               datasets: [{
                   data: result.data, // Y-axis data
                   backgroundColor: [
                       'rgba(255, 99, 132, 0.2)',
                       'rgba(54, 162, 235, 0.2)',
                       'rgba(255, 206, 86, 0.2)',
                       'rgba(257, 209, 76, 0.2)'
                   ],
                   borderColor: [
                       'rgba(255, 99, 132, 1)',
                       'rgba(54, 162, 235, 1)',
                       'rgba(255, 206, 86, 1)',
                       'rgba(257, 209, 76, 1)'

                   ],
                   borderWidth: 1
               }]
           },
           options: {
              aspectRatio: 2
           }
        });
     });
   }
   redirectToLeads() {
     console.log(this)
     this.env.services.action.doAction({
         type: 'ir.actions.act_window',
         name: 'Leads',
         res_model: 'crm.lead',
         views:[[false, "list"], [false, "form"]],
         target: 'current',
         domain : [["user_id", "=", session.uid],['type', '=', 'lead']]

     });
 }
 redirectToOpportunity(){
 this.env.services.action.doAction({
         type: 'ir.actions.act_window',
         name: 'Opportunity',
         res_model: 'crm.lead',
         views: [[false, "list"], [false, "form"]],
         target: 'current',
        domain : [["user_id", "=", session.uid],['type', '=', 'opportunity']]
       });
 }
 }
CrmDashboard.template = "crm_dashboard.CrmDashboard";
//  Tag name that we entered in the first step.
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
