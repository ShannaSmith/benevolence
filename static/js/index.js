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

const acctBtn = document.getElementById('new-acct');

function showCreateAcct (evt) {
    const form = document.getElementById('create-acct');
    if (form.style.display === 'none'){
        form.style.display = 'block';
    }else{
        form.style.display = 'none';
        acctBtn.classList.add("hidden"); 
    }
    
};
function showBtn(evt){
    const btn = document.getElementById("new-acct");
    btn.classList.remove('hidden');
};