$(function() {
	'use strict';

    /* SLIDE DOWNS */
    function slideDown(target) {
        $('html, body').animate({
            scrollTop: target.offset().top
          }, 500);
    };

    $('.slide-down-anchor').on('click', function(event) {
        event.preventDefault();
        var target = $($(this).data('href'));
        slideDown(target);
    });

    /* FORMSETS */

	var formset = $('.formset-content');
	var form_template = formset.find('.inserted-form').clone();
	var total_forms = formset.find('[id$=-TOTAL_FORMS]');

	// utility index updating function
    var updateElementIndex = function (elem, prefix, ndx) {
        var idRegex = new RegExp(prefix + "-(\\d+|__prefix__)-");
        var replacement = prefix + "-" + ndx + "-";

        if (elem.attr("for")) {
            elem.attr("for", elem.attr("for").replace(idRegex, replacement));
        }
        if (elem.attr("id")) {
            elem.attr("id", elem.attr("id").replace(idRegex, replacement));
        }
        if (elem.attr("name")) {
            elem.attr("name", elem.attr("name").replace(idRegex, replacement));
        }
    };

    // add new form
    $("#add-button").on('click', function() {
    	var idx = parseInt(total_forms.val());
    	var new_form = form_template.clone();
    	new_form.find('input, label, select').each(function() {
    		updateElementIndex($(this), 'form', idx);
    	});
        new_form.find('.form-order').html('#'+(idx+1));
    	formset.find('.dynamic-forms').append(new_form);
    	total_forms.val(idx+1);
    });

    // remove last form
    $("#remove-button").on('click', function() {
    	var forms = formset.find('.inserted-form');
    	var total = forms.length;
    	if (total > 1) {
    		forms.last().remove();
    		total_forms.val(total-1);
    	}
    });


    /* FILE INPUTS */
    $(document).on('change', 'input[type="file"]', function() {
        var input = $(this);
        var form = input.parents('.inserted-form');
        var fname = input.val().replace(/\\/g, '/').replace(/.*\//, '');

        // display filename in preview input
        form.find('.preview-input').val(fname);
        form.find('.categories-input-wrapper').find('select').select2();
        form.find('.categories-input-wrapper').show();
        // 
    });
});