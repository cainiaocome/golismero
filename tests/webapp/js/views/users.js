window.UsersView = Backbone.View.extend({
	tagName: 'div',
    className: '',
    initialize: function () {
        this.render();
    },

    render: function () {
		$(this.el).html(this.template({list:this.model.toJSON()}));
        return this;
    }

});