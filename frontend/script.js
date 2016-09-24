
$(function() {
  // We can attach the `fileselect` event to all file inputs on the page
  $(document).on('change', ':file', function() {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
  });
  
  var end = function() {
				$('.email').hide();
				$('.jumbotron' ).append("<div>Dziękujemy za skorzystanie z naszego serwisu</div>");
		}

  // We can watch for our custom `fileselect` event like this
  $(document).ready( function() {
	  $('.email').hide();
			  $( '#ok' ).click(function() {
				//$('#plik').val("");
				$('.email').show();
				$('.abc').hide();
		      });
		
		 $( '#no' ).click(function() {
				$('#plik').val("");
		});
	  
      $(':file').on('fileselect', function(event, numFiles, label) {

          var input = $(this).parents('.input-group').find(':text'),
              log = numFiles > 1 ? numFiles + ' files selected' : label;

          if( input.length ) {
              input.val(log);
          } else {
              if( log ){
				 // alert(log);
				  $('#plik').val(log);
			  }
			  
          }

      });
  });
  
});
