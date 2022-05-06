$(document).ready(function(){

	$('input[type="radio"]').on('change', function(e){
 //состояние $(this).prop('checked');
    var icon = $("input[type='radio'][name='status']:checked").val();
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'http://127.0.0.1:5000/api/registration-choices/${icon}', false ); // false for synchronous request
    xmlHttp.send( null );
    var as = xmlHttp.responseText;
    document.getElementById("mesto").innerHTML = as;
    });

});
