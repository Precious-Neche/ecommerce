let loading = document.querySelector('#page');

window.addEventListener('load', loads )

function loads(){
    setTimeout(() => {
        loading.classList.add('loader')
    }, 2000);
}