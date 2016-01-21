openerp.hr_payroll_period = function (instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    instance.web.hr_payroll_period = instance.web.hr_payroll_period || {};
    
    instance.web.views.add('tree_hr_payroll_period', 'instance.web.hr_payroll_period.PayrollPeriodTreeView');
    instance.web.hr_payroll_period.PayrollPeriodTreeView = instance.web.ListView.extend({
        init: function() {
            this._super.apply(this, arguments);
            this.fiscal_periods = [];
            this.periods_schedules = [];
            this.current_fiscal_period = null;
            this.current_period_schedule = null;
        },
        start:function(){
            var self= this;
            var tmp = this._super.apply(this, arguments);
            
            this.$el.parent().prepend(QWeb.render("PayrollPeriodTreeView", {widget: this}));
            
            this.$el.parent().find('.oe_hr_payroll_period_fiscal_period').change(function(){
                self.current_fiscal_period = this.value === '' ? null : parseInt(this.value);
                self.do_search(self.last_domain, self.last_context, self.last_group_by);
            });

            this.$el.parent().find('.oe_hr_payroll_period_periods_schedules').change(function(){
                self.current_period_schedule = this.value === '' ? null : parseInt(this.value);
                self.do_search(self.last_domain, self.last_context, self.last_group_by);
            });

            return $.when(tmp, this.load_fiscal_periods(), this.load_periods_schedules())
        },
        load_fiscal_periods : function(){
            var self = this;
            var defs = [];
            var select = this.$el.parent().find('.oe_hr_payroll_period_fiscal_period');
            select.children().remove().end();
            select.append(new Option('',''));
            var mod = new instance.web.Model("hr.payroll.period", this.dataset.context, this.dataset.domain);
            mod.call("list_fiscal_periods", []).then(function(result){
                for (i in result) {
                    opt = new Option(result[i][1], result[i][0]);
                    select.append(opt);
                }
            });
        },
        load_periods_schedules : function(){
            var self = this;
            var defs = [];
            var select = this.$el.parent().find('.oe_hr_payroll_period_periods_schedules');
            select.children().remove().end();
            select.append(new Option('',''));
            var mod = new instance.web.Model("hr.payroll.period", this.dataset.context, this.dataset.domain);
            mod.call("list_periods_schedules", []).then(function(result){
                for (i in result) {
                    opt = new Option(result[i][1], result[i][0]);
                    select.append(opt);
                }
            });
        },
        do_search: function(domain, context, groupBy){
            var self = this;
            this.last_domain = domain;
            this.last_context = context;
            this.last_group_by = groupBy;
            this.old_search = _.bind(this._super, this);
            return this.search_by_period_and_schedule();
        },
        search_by_period_and_schedule: function(){
            var self = this;
            var domain = [];
            if (self.current_period_schedule !== null) domain.push(['schedule_id','=', self.current_period_schedule]);
            if (self.current_fiscal_period !== null) domain.push(['fiscal_period_id','=', self.current_fiscal_period]);
            var compound_domain = new instance.web.CompoundDomain(self.last_domain, domain);
            self.dataset.domain = compound_domain.eval();
            return self.old_search(compound_domain, self.last_context, self.last_group_by);
        },

        do_activate_record: function (index, id, dataset, view) {
            this.active_period_id = id;
            this._super(index, id, dataset, view);
        },

        //Sobreescribimos este metodo para lanzar el wizard
        select_record:function (index, view) {
            var self = this;
            var model = new instance.web.Model("ir.model.data");
            var domain = [['name', '=', 'action_payroll_period_wizard']]
            _.delay(_.bind(function () {
                model.get_func("search_read")(domain, ['res_id']).pipe(_.bind(function(res){    
                    instance.session.rpc('/web/action/load', {'action_id': res[0]['res_id']})
                      .pipe(_.bind(function(result){
                            var action = result
                            var additional_context = {'period_id':self.active_period_id}
                            var ncontext = new instance.web.CompoundContext(additional_context, action.context || {});
                            action.context = ncontext;
                            this.do_action(action);
                      }, this))       
                }, self))
            }));
        },

    });
}
