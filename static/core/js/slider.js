const slider = document.querySelector('.slider');

function activate(e) {
  const items = document.querySelectorAll('.itemt');
  e.target.matches('.next') && slider.append(items[0])
  e.target.matches('.prev') && slider.prepend(items[items.length-1]);
}

document.addEventListener('click',activate,false);

// document.getElementById("loadContentButton").addEventListener("click", loadContent);

// function loadContent() {
//   fetch("new_content.html")
//     .then(response => response.text())
//     .then(data => {
//       document.getElementById("contentContainer").innerHTML = data;
//     });
// }