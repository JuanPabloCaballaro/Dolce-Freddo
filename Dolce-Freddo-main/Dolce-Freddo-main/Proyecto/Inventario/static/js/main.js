const menu = document.querySelector("#menu");
const abrir = document.querySelector("#abrir");
const cerrar = document.querySelector("#cerrar");
const contenido = document.querySelector("#contenido");

abrir.addEventListener("click", ()=>{
    menu.classList.add("visible");
    contenido.classList.add("hidden");

})
cerrar.addEventListener("click", ()=>{
    menu.classList.remove("visible");
    contenido.classList.remove("hidden");
})

const contendedor = document.querySelector(".contenedor-formularios");
const registrar = document.querySelector(".btn-registro");
const login = document.querySelector(".btn-login");

registrar.addEventListener("click", ()=>{
    contendedor.classList.add("active");
});

login.addEventListener("click", ()=>{
    contendedor.classList.remove("active");
});