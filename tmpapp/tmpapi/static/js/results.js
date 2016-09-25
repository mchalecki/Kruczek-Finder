$(function() {
    var inArea;
    var map = $('.map-image');
    var single_opts = {
                stroke: true,
                strokeColor: 'ff0000',
                strokeWidth: 5
            },
            all_opts = {
                fillColor: 'd0d0d0',
                fillOpacity: 0.2,
                stroke: true,
                strokeWidth: 5,
                strokeColor: 'ff0000',
                strokeOpacity: 0.4
            },
            initial_opts = {
                mapKey: 'data-name',
                isSelectable: false,
                onMouseover: function (data) {
                    inArea = true;
                    var self = $(this);
                    var clause_id = self.data('clause');
                    var clause_div = $('.clause[data-clause='+clause_id+']');
                    clause_div.show();
                },
                onMouseout: function (data) {
                    inArea = false;
                    var self = $(this);
                    var clause_id = self.data('clause');
                    var clause_div = $('.clause[data-clause='+clause_id+']');
                    clause_div.hide();
                }
            };

    opts = $.extend({}, all_opts, initial_opts, single_opts);
    map.mapster('unbind')
            .mapster(opts)
            .bind('mouseover', function () {
                if (!inArea) {
                    map.mapster('set_options', all_opts)
                            .mapster('set', true, 'all')
                            .mapster('set_options', single_opts);
                }
            }).bind('mouseout', function () {
        if (!inArea) {
            map.mapster('set', false, 'all');
        }
    });
});