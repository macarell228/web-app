$(document).ready(function(){

	var myCarousel = document.querySelector('#myCarousel')
    var carousel = new bootstrap.Carousel(myCarousel)

    /* var inputs = document.getElementsByClassName('my-input-class');
    for(var i = 0; i < inputs.length; i++) {
        inputs[i].required = false;
    } */

	var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

});