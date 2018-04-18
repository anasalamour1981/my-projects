openerp.base_odex = function (instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.web.odex = instance.web.odex || {};

    instance.web.client_actions.add('export_excel', 'instance.web.odex.exportExcel');


    instance.web.odex.exportExcel = openerp.Widget.extend({
        init: function(parent, context) {
            this._super(parent);
            // insert code to execute before rendering, for object
            // initialization
            this.context = context;
        },
        start: function() {
            var sup = this._super();
            // post-rendering initialization code, at this point
            // console.log(instance);
            var self = this;
            var c = instance.webclient.crashmanager;
            var workbook = this.context.context.workbook;
            instance.webclient.set_content_full_screen(true);
            instance.web.blockUI();
            this.session.get_file({
                url: '/web/base_odex/export',
                data: {
                    workbook: [workbook]
                },
                complete: instance.web.unblockUI(),
                error: c.rpc_error.bind(c)
            });
            
        },
    });

    /**
      * ------------------------------------------------------------
      * UserMenu
      * ------------------------------------------------------------
      * 
      * Add a link on the top user bar for write a full mail
      */
     instance.web.ComposeMessageTopButton = instance.web.Widget.extend({
         template:'mail.ComposeMessageTopButton',

         start: function () {
             this.$el.on('click', this.on_compose_message);
             this._super();
         },

         on_compose_message: function (event) {
             event.preventDefault();
             event.stopPropagation();
             var action = {
                 type: 'ir.actions.act_window',
                 res_model: 'mail.compose.message',
                 view_mode: 'form',
                 view_type: 'form',
                 views: [[false, 'form']],
                 target: 'new',
                 context: {},
             };
             instance.client.action_manager.do_action(action);
         },
     });

     instance.web.UserMenu.include({
         do_update: function(){
             var self = this;
             this._super.apply(this, arguments);
             this.update_promise.then(function() {
                 var mail_button = new instance.web.ComposeMessageTopButton();
                 mail_button.appendTo(instance.webclient.$el.parents().find('.oe_systray'));
                 openerp.web.bus.trigger('resize');  // Re-trigger the reflow logic
             });
         },
     });


}