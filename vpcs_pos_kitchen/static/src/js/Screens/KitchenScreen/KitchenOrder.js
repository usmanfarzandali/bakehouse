odoo.define('vpcs_pos_kitchen.KitchenOrder', function(require){
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { posbus } = require('point_of_sale.utils');
    const { useRef } = owl.hooks;


    class KitchenOrder extends PosComponent {
        constructor() {
            super(...arguments);
            this.time_interval = false;
            this.$waiting_tms = useRef('waiting_time');
        }
        get creation_date() {
            return moment(this.props.order.creation_date).format('hh:mm') || '';
        }
        willPatch() {
            posbus.off('render-kitchen-order', this);
        }
        patched() {
            posbus.on('render-kitchen-order', this, this.render);
        }
        _compute_waiting_time() {
            if(!this.$waiting_tms.el) return;
            let creation_date = this.$waiting_tms.el.dataset.creation_date;
            const format = "YYYY-MM-DD hh:mm:ss";
            let ms = moment(moment(), format).diff(creation_date, format);
            let duration = moment.duration(ms);
            let time = "";
            if (duration.hours() > 0) {
                time = duration.hours() + ":";
            }
            time += duration.minutes() + ':' + duration.seconds();
            $(this.$waiting_tms.el).text(time);
        }
        mounted() {
            posbus.on('render-kitchen-order', this, this.render);
            this.time_interval = setInterval(() => {
                this._compute_waiting_time();
            }, 1000);
        }
        willUnmount() {
            posbus.off('render-kitchen-order', this);
            clearInterval(this.time_interval);
        }
    }
    KitchenOrder.template = 'KitchenOrder';

    Registries.Component.add(KitchenOrder);

    return KitchenOrder;
});