odoo.define('vpcs_pos_kitchen.Chrome', function(require){
    'use strict';
    
    const Chrome = require('point_of_sale.Chrome');
    const Registries = require('point_of_sale.Registries');
    const { posbus } = require('point_of_sale.utils');
    const { useListener } = require('web.custom_hooks');
    var session = require('web.session');
    const iface_pos_tone = _.contains(session.module_list, 'vpcs_pos_kitchen_tone.KitchenTones');
    const CHANEL = "pos.order.synch";

    const PosKitchenChrome = (Chrome) =>
        class extends Chrome {
            constructor() {
                super(...arguments);
                useListener('play-kitchen-sound', this.__onPlayKitchenSound);
                this.env.services.bus_service.call('bus_service', 'addChannel', 'pos.order.synch');
                this.env.services.bus_service.call('bus_service', 'onNotification', this, this._onNotification);
            }
            __onPlayKitchenSound({ detail: name, custom_sound = false }) {
                let src;
                if (custom_sound && iface_pos_tone) {
                    this.play_custom_tone();
                } else {
                    if (name === 'error') {
                        src = "/point_of_sale/static/src/sounds/error.wav";
                    } else if (name === 'bell') {
                        src = "/point_of_sale/static/src/sounds/bell.wav";
                    } else if (name === 'tin') {
                        src = "/vpcs_pos_kitchen/static/src/sounds/tin.wav";
                    }
                    let audio = new Audio(src);
                    audio.autoplay = true;
                    $('body').append(audio);
                }
            }
            play_custom_tone(){
                const id = this.env.pos.config.tone_id[0]
                _.each(this.env.pos.sounds, function(storedSound) {
                    if (storedSound['id'] == id) {
                        let src = 'data:audio/mpeg;base64,' + storedSound['music_file']
                        let audio = new Audio(src);
                        audio.autoplay = true;
                        $('body').append(audio);
                    }
                });
            }
            get startScreen() {
                if (this.env.pos.config.iface_is_kitchen) {
                    return { name: 'KitchenScreen', props: {'KitchenScreen': true} };
                } else if (this.env.pos.config.iface_floorplan) {
                    const table = this.env.pos.table;
                    return { name: 'FloorScreen', props: { floor: table ? table.floor : null } };
                }else {
                    return super.startScreen;
                }
            }
            get isKitchenScreenShown() {
                return this.mainScreen.name === 'KitchenScreen';
            }
            _onNotification(notification) {
                var channel = notification[0] ? notification[0][0] ? notification[0][0] : false : false;
                var message = notification[0] ? notification[0][1] ? notification[0][1] : false : false;
                if ((Array.isArray(channel) && (channel[1] === 'pos.order.synch'))) {
                    if (message) {
                        var result = _.omit(message, 'order_status');
                        if (message.order_status == 'new_order') {
                            this.env.pos.db.synch_orders.push(result);
                        } else if (message.order_status == 'update_order') {
                            var update_orders = _.filter(this.env.pos.db.synch_orders, function(sync_order) {
                                return sync_order.order_uid != result.order_uid;
                            });
                            update_orders.push(result);
                            this.env.pos.db.synch_orders = update_orders;
                        } else if (message.order_status == 'remove_order') {
                            var update_orders = _.filter(this.env.pos.db.synch_orders, function(sync_order) {
                                return sync_order.order_uid != result.order_uid;
                            });
                            this.env.pos.db.synch_orders = update_orders;
                        } else if (message.order_status == 'orderline_state') {
                            _.each(this.env.pos.db.synch_orders, function(sync_order) {
                                if (sync_order.order_uid == result.order_uid) {
                                    sync_order.order_data = result.order_data;
                                }
                            });
                            this.set_orderline_state(result.order_data);
                        }
                        posbus.trigger('render-kitchen');
                    }
                }
            }
            get_order_by_id(data) {
                var uid = data.uid;
                var orders = this.env.pos.get_order_list();
                for (var i = 0; i < orders.length; i++) {
                    if (orders[i].uid === uid) {
                        return orders[i];
                    }
                }
                return undefined;
            }
            set_orderline_state(result) {
                var data = JSON.parse(result);
                var lines = data['lines'];
                var data = JSON.parse(result);
                var order = this.get_order_by_id(data),
                    orderlines = order && order.get_orderlines() || [];
                if (!_.isEmpty(orderlines)) {
                    _.each(orderlines, function(line) {
                        _.each(lines, function(l) {
                            if (line.id == l.id) {
                                line.set_state(l.state);
                            }
                        });
                    });
                }
            }
        }

    Registries.Component.extend(Chrome, PosKitchenChrome);

    return Chrome;
});