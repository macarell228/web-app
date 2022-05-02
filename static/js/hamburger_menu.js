$(document).ready(function(){

	// MOSTRANDO Y OCULTANDO MENU
	$('#button-menu').click(function(){
		if($('#button-menu').attr('class') == 'fa fa-bars' ){

			$('.navigation').css({'width':'100%', 'background':'rgba(0,0,0,.5)'}); // Mostramos al fondo transparente
			$('#button-menu').removeClass('fa fa-bars').addClass('fa fa-close'); // Agregamos el icono X
			$('.navigation .menu').css({'left':'0px'}); // Mostramos el menu

		} else{

			$('.navigation').css({'width':'0%', 'background':'rgba(0,0,0,.0)'}); // Ocultamos el fonto transparente
			$('#button-menu').removeClass('fa fa-close').addClass('fa fa-bars'); // Agregamos el icono del Menu
			$('.navigation .submenu').css({'left':'-320px'}); // Ocultamos los submenus
			$('.navigation .menu').css({'left':'-320px'}); // Ocultamos el Menu

		}
	});

	// MOSTRANDO SUBMENU
	$('.navigation .menu > .item-submenu a').click(function(){
		
		var positionMenu = $(this).parent().attr('menu'); // Buscamos el valor del atributo menu y lo guardamos en una variable
		console.log(positionMenu); 

		$('.item-submenu[menu='+positionMenu+'] .submenu').css({'left':'0px'}); // Mostramos El submenu correspondiente

	});

	// OCULTANDO SUBMENU
	$('.navigation .submenu li.go-back').click(function(){

		$(this).parent().css({'left':'-320px'}); // Ocultamos el submenu

	});

});