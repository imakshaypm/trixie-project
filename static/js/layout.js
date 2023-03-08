$(document).ready(function () {
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });
    var activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
        $('#myTab a[href="' + activeTab + '"]').tab('show');
    }

    /*
      Temporarily disable hyperlinks to see menu work
    */

    $('a.nav-link').on('click', function (e) {
        $(this).parent().addClass('active-link').siblings().removeClass('active-link');
    });
});