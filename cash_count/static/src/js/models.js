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
                                      [['role','in',['cashier','manager']]])
                }).then(function(cashiers){
                    self.set('cashiers',cashiers)
                    session_id = self.get('pos_session').id
                    return self.fetch('cash.count.cashier.session',
                                      [],
                                      [['state','=','opened'],
                                      ['session_id','=',session_id]]) 
                }).then(function(session){
                    if (!_.isEmpty(session)){
                        self.set('cashier_session',session[0])
                        self.set_current_cashier(session[0].cashier_id[0]);
                    }
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
            XReport.set('cashier_session_id',this.get('cashier_session').id);
            XReport.set('pos_session_id',this.get('pos_session').id);
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
        exportAsJSON: function(){
            return {
                'instrument_id':this.get('instrument').id,
                'journal_id': this.get('instrument').journal_id,
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
                'cashier_session_id': null,
                'pos_session_id': null,
                'printer_id': null,
                'printer_serial': null,
                'number': null,
                'date': null,
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
                'cashier_session_id': this.get('cashier_session_id'),
                'pos_session_id': this.get('pos_session_id'),
                'printer_id': this.get('printer_id'), //WARNING need implementation
                'date': this.get('date'),
                'number': this.get('number'),
                'printer_serial': this.get('printer_serial'),
                'lines' : lines, 
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