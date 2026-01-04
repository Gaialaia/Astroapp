let cq = 150;

let contents = document.querySelectorAll(".description");
contents.forEach(content => {
    if(content.textContent.length < cq) {
        content.nextElementSibling.style.display = "none";
    }
    else {
        let displayText = content.textContent.slice (0,cq);
        let moreText = content.textContent.slice(cq);
        content.innerHTML = `
        ${displayText}<span class="dots">...</span>
        <span class="hide more"> ${moreText} </span>`
    }

});

function readMore(btn) {
    let post = btn.parentElement;
    post.querySelector(".dots").classList.toggle("hide");
    post.querySelector(".more").classList.toggle("hide");
    btn.textContent == "Read More" ? btn.textContent = "Read Less" : btn.textContent = "Read More";

}













