openerp.web_menu_search = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    var MenuSearch = instance.web.Widget.extend({
        template: "MenuSearch",
        init: function(parent) {
            this.enter_value = "";
            this._super(parent);
        },
        start: function() {
            this._super();
            this.do_search();
            
        },
        open_action: function(action_name){
           
        },
        do_search: function(value){
          var self = this;
          return new instance.web.Model("ir.ui.menu").get_func("get_access_menus")(self.session.uid).pipe(
                    _.bind(function(res) {
                    var auto_list = []
                    var test_list = []
                    self.set({'menus': res})
                    for (menu in res){
                        menu_obj = res[menu]
                        menu_id = menu_obj['id']
                        menu_name = menu_obj['name']
                        menu_action = menu_obj['action']
                        if (menu_action != false){
                            //action_id = menu_action.split(",")[1]
                            href = "#menu_id="+menu_id+"&action="+menu_action
                            disp_value = {
                                'value': href,
                                'label': menu_name
                            }
                            test_list.push(href)
                            auto_list.push(disp_value)
                        }
                    }
                    $('input#menu_name').autocomplete(
                                                      {
                                                      source: auto_list,
                                                      focus: function(event, ui) {
                                                                     $("#menu_name").val(ui.item.label);
                                                                     return false;
                                                                                  },
                                                      select: function (event, ui) {
                                                                    window.location.href = ui.item.value;
                                                                    return false;
                                                                                    },
                                                      //search: function( event, ui ) {
//                                                                    alert(JSON.stringify(ui))
//                                                      }
                                                      });
                    
                    
                    
                    
                    function lightwell(request, response) {
                        function hasMatch(s) {
                            return s.toLowerCase().indexOf(request.term.toLowerCase())!==-1;
                        }
                        var i, l, obj, matches = [];
                
                        if (request.term==="") {
                            response([]);
                            return;
                        }
                           
                        for  (i = 0, l = projects.length; i<l; i++) {
                            obj = projects[i];
                            if (hasMatch(obj.label) || hasMatch(obj.desc)) {
                                matches.push(obj);
                            }
                        }
                        response(matches);
                    }
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
            }, this));
        },
    });
    instance.web.UserMenu.include({
        init: function(parent) {
            var self = this;
            this._super.apply(this,arguments);
        },
        start: function(){
            var self = this;
            this._super.apply(this,arguments);
            var p = self.getParent();
            var menu_search = new MenuSearch(this);
            menu_search.insertBefore(p.$el.find('.oe_topbar'));
        },
    });
};
