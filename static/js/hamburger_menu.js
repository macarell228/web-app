$(document).ready(function(){

	$('#button-menu').click(function(){
		if($('#button-menu').attr('class') == 'fa fa-bars' ){

			$('.navigation').css({'width':'150%', 'background':'rgba(0,0,0,.5)'});
			$('#button-menu').removeClass('fa fa-bars').addClass('fa fa-close');
			$('.navigation .menu').css({'left':'0px'});

		} else{

			$('.navigation').css({'width':'0%', 'background':'rgba(0,0,0,.0)'});
			$('#button-menu').removeClass('fa fa-close').addClass('fa fa-bars');
			$('.navigation .submenu').css({'left':'-320px'});
			$('.navigation .menu').css({'left':'-320px'});

		}
	});

	$('.navigation .menu > .item-submenu a').click(function(){
		
		var positionMenu = $(this).parent().attr('menu');
		console.log(positionMenu); 

		$('.item-submenu[menu='+positionMenu+'] .submenu').css({'left':'0px'});

	});

	$('.navigation .submenu li.go-back').click(function(){

		$(this).parent().css({'left':'-320px'});

	});

	var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

});