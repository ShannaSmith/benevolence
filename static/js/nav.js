$(document).ready(function () {
    $("ul.navbar-nav > a").click(
      function (e) {
        $("ul.navbar-nav > a").removeClass(
          "active");
        $("ul.navbar-nav > a").css(
          "color", "");

        $(this).addClass("active");
        $(this).css("color", "red");
    });
});