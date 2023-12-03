function rate(element) {
    console.log(element.title);

    fetch(`/shop/api/productos/${element.title}`)
        .then(res => res.json())
        .then(res => {
            const prod_rating = res.rating ? Math.floor(res.rating.rate) : 0;

            let starsHTML = '';
            for (let i = 0; i < 5; i++) {
                if (i < prod_rating) {
                    starsHTML += '<span class="fa fa-star checked"></span>';
                } else {
                    starsHTML += '<span class="fa fa-star"></span>';
                }
            }
            element.innerHTML = starsHTML;
        })
        .catch(error => alert(`${error}`));
}

document.addEventListener('DOMContentLoaded', () => {
    const span_for_stars = document.querySelectorAll('span.sp');

    span_for_stars.forEach(ele => {
        rate(ele);
    });
});
