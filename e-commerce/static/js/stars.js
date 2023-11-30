function rate(element) {
    console.log(element.title);
    fetch(`/api/productos/${element.title}`)
        .then(res => res.json())
        .then(res => console.log(res.rating))
        .catch(error => alert(`${error}`));
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('Script executed!');
    
    const span_for_stars = document.querySelectorAll('span.sp');
    span_for_stars.forEach(ele => {
        ele.innerHTML = `
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
        `;
    });
});
