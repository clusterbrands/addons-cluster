function cash_count_models(instance, module){

    module.PosModel = module.PosModel.extend({
        initialize:function(session,attributes){
            this._super(session,attributes);
            this.set({
                'currentXReport':null,
                'XReports': new module.XReportCollection(),
            })
        },
        new_x_report: function(){
            var XReport = new module.XReport({});
            XReport.set('cashier',this.get('current_cashier'));
            XReport.set('user',this.get('user'));
            XReport.set('pos_config',this.get('pos_config'));
            this.set('currentXReport',XReport);
        },
    })

    module.XReportLine = Backbone.Model.extend({
        initialize :function(attrs){
            this._super(attrs);
            this.set({
                'instrument':null,
                'amount':0,
            })
        },
        get_amount: function(){
            return this.get('amount');
        },
        set_amount: function(newAmount){
            var amount = parseFloat(newAmount);
            if (amount >= 0)
                this.set('amount',amount); 
        },
        get_instrument: function(){
            instrument = this.get('instrument');
            return instrument.journal_name + ' - ' + instrument.code;
        },
    });

    module.XReportLineCollection = Backbone.Collection.extend({
        model: module.XReportLine,
    });

    module.XReport = Backbone.Model.extend({
        initialize :function(attrs){
            this._super(attrs);
            this.set({
                'cashier': null,
                'user':null,
                'pos_config':null,
                'date':null,
                'time':null,
                'printer_number':null,
                'lines': new module.XReportLineCollection(),
            })
            this.selectedLine = null;
            return this;
        },
        addLine: function(instrument){
            lines = this.get('lines');
            l = lines.where({instrument:instrument});
            if (l.length == 0){
                line = new module.XReportLine({});
                line.set('instrument',instrument);
                lines.add(line);
            }else{
                l[0].trigger('focus');
            }
        },
        selectLine: function(line){
            this.selectedLine = line;
        },
        getSelectedLine: function(){
            return this.selectedLine;
        },
        getTotal: function(){
            return (this.get('lines')).reduce((function(sum, line){
                return sum + line.get_amount();
            }), 0);
        }
    });

    module.XReportCollection = Backbone.Collection.extend({
        model: module.XReport,
    })

}