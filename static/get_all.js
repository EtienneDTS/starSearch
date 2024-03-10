const start = document.querySelector(".start")
const end = document.querySelector(".end")
const next = document.querySelector(".next")
const previous = document.querySelector(".previous")
const page = parseInt(document.querySelector(".current_page").getAttribute("value"))
const maxPage = parseInt(document.querySelector(".max_page").getAttribute("value"))

if (page === 1) {

    start.style.color = "#666"
    previous.style.color = "#666"

    start.addEventListener("click", (e)=>{
        e.preventDefault()
    })

    previous.addEventListener("click", (e)=>{
        e.preventDefault()
    })
}

if (page === maxPage) {

    next.style.color = "#666"
    end.style.color = "#666"
    next.addEventListener("click", (e)=>{
        e.preventDefault()
    })

    end.addEventListener("click", (e)=>{
        e.preventDefault()
    })
}