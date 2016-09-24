$(function() {
	'use strict';

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
    	new_form.find('input, label').each(function() {
    		updateElementIndex($(this), 'form', idx);
    	});
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
});