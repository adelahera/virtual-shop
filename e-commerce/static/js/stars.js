function initStars(element) {
    console.log('Elemento recibido:', element);

    fetch(`/shop/api/productos/${element.title}`)
        .then(res => res.json())
        .then(res => {
            const prod_rating = res.rating ? Math.floor(res.rating.rate) : 0;
            const prod_count = res.rating ? res.rating.count : 0;
            console.log(`El producto ${element.title} tiene una valoración de ${prod_rating} estrellas con un total de ${prod_count} valoraciones.`);
            let starsHTML = '';
            for (let i = 0; i < 5; i++) {
                const starClass = i < prod_rating ? 'checked' : '';
                starsHTML += `<span class="fa fa-star ${starClass}" data-rating="${i + 1}"></span>`;
            }
            element.innerHTML = starsHTML;

        })
        .catch(error => alert(`${error}`));
}

function sendRating(element, userIsAuthenticated) {

    if(userIsAuthenticated == true){
        const stars = element.target.parentNode.querySelectorAll('.fa-star');

        fetch(`/shop/api/productos/${element.target.parentNode.title}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error en la solicitud: ${response.statusText}`);
                }
                return response.json();
            })
            .then(productData => {
                console.log("id del producto: ", productData.id);

                const prod_count = productData.rating ? productData.rating.count : 0;
                const newCount = parseInt(prod_count) + 1;

                stars.forEach(star => {
                    star.addEventListener('click', () => {
                        const clickedRating = parseFloat(star.getAttribute('data-rating'));
                        console.log(`Valoración enviada: ${clickedRating}`);
                        console.log(`Numero de votos: ${prod_count}`);

                        fetch(`/shop/api/productos/${productData.id}`, {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + 'supersecret',
                            },
                            body: JSON.stringify({
                                title: productData.title,
                                price: productData.price,
                                description: productData.description,
                                category: productData.category,
                                rating: {  
                                    rate: clickedRating,
                                    count: newCount,
                                },
                            }),
                        })
                        .then(ratingResponse => {
                            if (!ratingResponse.ok) {
                                throw new Error(`Error en la solicitud: ${ratingResponse.statusText}`);
                            }
                            return ratingResponse.json();
                        })
                        .then(updatedProduct => {
                            console.log('Valoración enviada con éxito:', updatedProduct);
                            console.log(`El producto ${element.title} tiene una valoración de ${updatedProduct.rating.rate} estrellas con un total de ${updatedProduct.rating.count} valoraciones.`);
                            initStars(element.target.parentNode);
                        })
                        .catch(error => {
                            alert(`Error al enviar la valoración: ${error.message}`);
                        });
                    });
                });
            })
            .catch(error => {
                alert(`${error}`);
            });
    }
    else{
        alert("You must be logged in to rate a product");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const span_for_stars = document.querySelectorAll('span.sp');

    span_for_stars.forEach(ele => {
        initStars(ele);
    });
});
