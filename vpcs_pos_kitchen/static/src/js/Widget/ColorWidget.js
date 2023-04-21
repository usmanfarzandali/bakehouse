odoo.define('vpcs_pos_kitchen.ColorPicker', function(require) {
    "use strict";

    var core = require('web.core');
    var field_registry = require('web.field_registry');
    var fields = require('web.basic_fields');

    var qweb = core.qweb;

    var FieldColorPicker = fields.FieldChar.extend({
        template: 'FieldColorPicker',
        widget_class: 'oe_form_field_color',
        _renderEdit: function() {
            var value = this.value;
            var $input = this.$('input');
            $input.val(value);
            this.$el.colorpicker({
                format: 'rgba',
                horizontal: true,
            });
            this.$input = $input;
            this.$el.find('i').addClass('oe_color_picker_button');
        },
        _renderReadonly: function() {
            var value = this._formatValue(this.value);
            var $btn = $('<i />')
            .addClass('colorpicker-selectors-color')
            .css('background-color', value).data('class', 'oe_color_picker_button');
            this.$el.html(qweb.render('VisibleFieldColorPicker', { color: value}));
        },
        _getValue: function() {
            var $input = this.$('input');
            var value = $input.val();
            var falg = /^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+(?:\.\d+)?))?\)$/i.test(value);
            if (!falg) return;
            return $input.val();
        },
    });

    field_registry
        .add('colorpicker', FieldColorPicker);

        return {
            FieldColorPicker: FieldColorPicker
        }
});