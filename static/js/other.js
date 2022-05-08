$(document).ready(function(){
    var x = 0;

    function addInput() {
        if (x < 10) {
        var str = '<p>{{ for.prof_devop_list.date.label }}</p><input type="date"><input type="text" placeholder="{{ form.prof_devop_list.description.label }}"><p>{{ for.prof_devop_list.during.label }}</p><input type="range"> <div id="input' + (x + 1) + '"></div>';
        document.getElementById('input' + x).innerHTML = str;
        x++;
      } else
      {
        alert('STOP it!');
      }
    }

	var myCarousel = document.querySelector('#myCarousel')
    var carousel = new bootstrap.Carousel(myCarousel)

	var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

});