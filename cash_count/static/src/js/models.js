function cash_count_models(instance, module){

    module.PosModel = module.PosModel.extend({
        initialize:function(session,attributes){

            this._super(session,attributes);
            this.set({
                'currentXReport':null,
            });
        },
        load_server_data : function(){
            var self = this
            var loaded = this._super()
                .then(function(){
                    return self.fetch('hr.employee',
                                      ['name','username','image_small'],
                                      [['role','=','cashier']])
                }).then(function(cashiers){
                    self.set('cashiers',cashiers)
                    session_id = self.get('pos_session').id
                    return self.fetch('cash.count.cashier.session',
                                      ['cashier_id'],
                                      [['state','=','opened'],
                                      ['session_id','=',session_id]]) 
                }).then(function(session){
                    if (!_.isEmpty(session))
                        self.set_current_cashier(session[0].cashier_id[0]);
                });
            return loaded
        },
        set_current_cashier: function(cashier_id){
            cashiers = this.get('cashiers')
            cashier = {}
            cashier = _(cashiers).find(function(c) {
                return c.id = cashier_id;
            })
            if (!_.isEmpty(cashier))
                this.set('cashier',cashier)
        },
        new_x_report: function(){
            var XReport = new module.XReport({});
            XReport.set('cashier',this.get('current_cashier'));
            XReport.set('user',this.get('user'));
            XReport.set('pos_config',this.get('pos_config'));
            XReport.set('opening_balance',this.get('opening_balance'));
            XReport.set('date',instance.web.date_to_str(new Date()));
            this.set('currentXReport',XReport);
        },
        save_x_report: function(){
            report = this.get('currentXReport')
            console.debug(report.exportAsJSON());                    
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
        exportAsJSON: function(){
            return {
                'instrument_id':this.get('instrument').id,
                'amount': this.get('amount'),
            }
        }
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
                'opening_balance':null,
                'date':null,
                'time':null,
                'printer_serial':null,
                'report_number':null,
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
        },
        exportAsJSON : function(){
            var lines = []
            this.get('lines').each(_.bind(function(line){
                return lines.push(line.exportAsJSON());
            },this));
            return {
                'cashier_id': this.get('cashier').id,
                'user_id': this.get('user').id,
                'pos_config': this.get('pos_config').id,
                'opening_balance': this.get('opening_balance'),
                'date': this.get('date'),
                'time': this.get('time'),
                'printer_serial': this.get('printer_serial'),
                'report_number': this.get('report_number'),
                'payment_instruments' : lines, 
            }
        }   

    });

    module.XReportCollection = Backbone.Collection.extend({
        model: module.XReport,
    })

    module.Cashier = Backbone.Model.extend({
        defaults:{
            'username': '',
            'password':'',
        },
        initialize :function(attrs){
            this._super(attrs);
        },
    });

}