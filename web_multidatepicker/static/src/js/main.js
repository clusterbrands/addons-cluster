openerp.hr_calendar = function(instance){
    var QWeb = instance.web.qweb;
    instance.hr_calendar.Calendar = instance.web.form.AbstractField.extend({
        init: function() {
            this._super.apply(this, arguments);
            this.set("value", "");
        },
        start: function() {
            var self = this;
            this.on("change:effective_readonly", this, function() {
                self.display_field();
                self.render_value();
            });
            self.display_field();
            return this._super();         
        },
        display_field: function(){
            var self = this;
            this.$el.html(QWeb.render("Calendar", {widget: this}));
            if (this.get('effective_readonly')){
                this.$('.calendar').multiDatesPicker({disabled:true});
            }else{
                this.$('.calendar').multiDatesPicker({disabled:false, onSelect: function(dateText){
                    dates = self.$('.calendar').multiDatesPicker('getDates');
                    self.internal_set_value(dates);                   
                }});
            }
        },
        render_value: function() {
            var dates = this.get('value') || [];
            if (dates.length > 0)
                this.$('.calendar').multiDatesPicker('addDates',eval(dates));
        },
    });
    instance.web.form.widgets.add('calendar', 'instance.hr_calendar.Calendar');
}
