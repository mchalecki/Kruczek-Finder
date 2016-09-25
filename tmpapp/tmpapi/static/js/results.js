$(function() {
    /* autoslide on enter */
    setTimeout(function() {
        $('html, body').animate({
            scrollTop: $('main').offset().top
        }, 500);
    }, 1000);

    /* mapster */
    var inArea;
    var current;
    var map = $('.map-image');
    var single_opts = {
            stroke: true,
            strokeColor: '1abc9c',
            strokeWidth: 4
        };
    var all_opts = {
            fillColor: 'd0d0d0',
            fillOpacity: 0.2,
            stroke: true,
            strokeWidth: 4,
            strokeColor: '1abc9c',
            strokeOpacity: 0.75
    };
    var initial_opts = {
        mapKey: 'data-name',
        isSelectable: false,
    };
    var opts = $.extend({}, all_opts, initial_opts, single_opts);
    map.mapster(opts);

    /* using mapster */
    $('.clause').on('mouseover', function() {
        var self = $(this);
        var clause_id = self.data('clause');
        current = clause_id.toString();
        map.mapster('set_options', all_opts)
                       .mapster('set', true, current)
                       .mapster('set_options', single_opts);
    });
    $('.clause').on('mouseout', function() {
        map.mapster('set', false, current);
        console.log("out");
    });
    
    /* fixed on scroll */
    var semi_fixed_item = $('.clauses-col');
    var offset = semi_fixed_item.offset().top;
    var left_col_height = $('.image-col').height();
    $(window).scroll(function() {
        //console.log($(window).scrollTop());
        //console.log(semi_fixed_item.offset.top);
        if($(window).scrollTop() > offset) {
            var margin = $(window).scrollTop() - offset;
            if (margin + semi_fixed_item.height() <= left_col_height) {
                semi_fixed_item.css('margin-top',margin+'px');
            }
        } else {
            semi_fixed_item.css('margin-top','0');
        }  
    });
});