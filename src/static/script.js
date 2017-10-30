function setup(){

// Set up loading spinner
$body = $("body");
$(document).on({
  ajaxStart: function() { $body.addClass("loading");    },
  ajaxStop: function() { $body.removeClass("loading"); }    
});

// Get comments, generate download button when complete
$( "#url-form" ).submit(function( event ) {

  $("#download").empty()
  $("#error").empty()

  var form = $(this);
  $.ajax({ 
    url   : form.attr('action'),
    type  : form.attr('method'),
    data  : form.serialize(), // data to be submitted
    success: function(response){
      if (response.error) {
        console.log(response.error)
        $("<p class=\"error-message\">" + response.error + "</p>").appendTo("#error");    
      
      } else {
        var downloadLink = "<a class=\"download-button\" href=\"data:application/csv;charset=utf-8," + 
          encodeURIComponent(response)  + "\" download=\"comments.csv\">" + 
          "<i class=\"material-icons\">&#xE2C4</i> Download Comments</a>"      

        $(downloadLink).appendTo("#download");
      }
    },
    error: function(error) {
      alert("error")
    }
  });
  event.preventDefault();
});

}
