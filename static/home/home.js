const menuOpen = document.querySelector(".menuOpen")
const menuList = document.querySelector(".listMenu")

menuList.addEventListener("click", ()=>{
    console.log("clicked")
    menuOpen.classList.toggle('open')
    console.log(menuOpen)
})