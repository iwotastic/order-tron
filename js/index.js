const $ = q => document.querySelector(q)

let pageNumber = 0
const greenDaysInTransit = 6
const yellowDaysInTransit = 11

const refresh = async function () {
  $("#table").innerHTML = "Please wait, loading..."

  resp = await fetch("/order_overview/html/_/get?page=" + pageNumber)
  newHTML = await resp.text()

  $("#table").innerHTML = newHTML
}

$("#next-page").addEventListener("click", ev => {
  pageNumber++
  $("#page-number").textContent = pageNumber + 1

  if (pageNumber != 0) {
    $("#prev-page").disabled = false
  }

  refresh()
})

$("#prev-page").addEventListener("click", ev => {
  pageNumber--
  $("#page-number").textContent = pageNumber + 1

  if (pageNumber == 0) {
    $("#prev-page").disabled = true
  }

  refresh()
})

$("#download").addEventListener("click", ev => {
  open("/order_overview/csv/_/data?page=" + pageNumber, "_blank")
})

refresh()