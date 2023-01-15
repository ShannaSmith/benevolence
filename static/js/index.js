let acctBtn = document.getElementById('new-acct');

function showCreateAcct (evt) {
    const form = document.getElementById('create-acct');
    console.log('print form>>>>>', form)
        form.style.display = 'block';
        form.classList.remove('hidden');
        acctBtn.classList.add("hidden");     
};
function showBtn(evt){
    const btn = document.getElementById("new-acct");
    btn.classList.remove('hidden'); //<<<<<may need to change to css visibilty
};

const navContainer = document.getElementById("navbarNavAltMarkup");
const links = navContainer.getElementsByClassName("be-link");
console.log('current url>>>>>>', window.location.pathname)
console.log("nav links>>>>>>>>>>>>>>", links)
for (let i = 0; i < links.length; i++){
    const href = links[i].getAttribute('href')
    console.log('printout href>>>>>>>>', href);
    if (href == window.location.pathname) {
        links[i].classList.add('active')
    }
}
let logBtn = document.getElementById('logIn');
function showLgInBtn(evt){
    const btn = document.getElementById("logIn");
    btn.classList.remove('hidden'); 
}

function showLogIn (evt) {
    const form = document.getElementById("login-frm");
    console.log('print form>>>>>', form)
        form.style.display = 'block';
        form.classList.remove('hidden');
        logBtn.classList.add("hidden");     
};

$('.alert').alert()
