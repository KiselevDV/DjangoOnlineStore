const form = document.querySelector('#payment-form');
// Ключ из самого приложения Stripe
const stripe = Stripe('pk_test_51JOnsiC11ED4v6Z5XiJxbOm76yIWIYlNvMRIKFNSaoHc4cskmCYEuue69wdyR6khty7Z3G1GSTQAEnUV0LAGutDN00J0gANg4f');
const elements = stripe.elements();  // для последующей работы с элементами, например добавить стили
const style = {
    base: {
        color: "#32325d",
    }
};

const card = elements.create("card", {style: style});
card.mount("#card-element");
// on('change' - реагирует на любое изменение
card.on('change', function (event) {
    const displayError = document.querySelector('#card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
});
// Событие на кнопке 'submit' в форме
form.addEventListener('submit', function (ev) {
    ev.preventDefault();  // отменяем базовое поведение формы
    // Элемент с data-secret="{{ client_secret }}"
    const clientSecret = document.querySelector('#card-button')
    // Подтвеждение платежа
    stripe.confirmCardPayment(clientSecret.dataset.secret, {
        payment_method: {
            card: card,
            // Добавить имя в billing_details
            billing_details: {
                name: document.querySelector('#card-button').dataset.username
            }
        }
    }).then(function (result) {
        // После прохождения запроса получаем ошибку
        if (result.error) {
            // Show error to your customer (e.g., insufficient funds)
            console.log(result.error.message);
            // Или всё успешно
        } else {
            // The payment has been processed!

            // Из документации Django, для работы с csrf_token
            if (result.paymentIntent.status === 'succeeded') {
                function getCookie(name) {
                    let cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
                        const cookies = document.cookie.split(';');
                        for (let i = 0; i < cookies.length; i++) {
                            const cookie = cookies[i].trim();
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }

                const csrftoken = getCookie('csrftoken');


                // Инициируем форму по name='order'
                const formData = new FormData(document.forms.order);
                // добавить к пересылке ещё пару ключ - значение
                // Имя плательщика и csrf token
                formData.append("first_name", document.querySelector('#card-button').dataset.username);
                formData.append("csrfmiddlewaretoken", csrftoken)

                // Создаём XML и отправляем post запрос
                const xhr = new XMLHttpRequest();
                // Представление обрабатывающее запрос на оплату, по маршруту /payed-online-order/
                xhr.open("POST", "/payed-online-order/");
                xhr.send(formData);  // отправляем всё из formData
                xhr.onreadystatechange = function () {
                    // Если всё удачно - xhr.readyState == 4
                    if (xhr.readyState == 4) {
                        // Перенаправляем пользователя на localhost
                        window.location.replace("http://127.0.0.1:8000");
                        alert('Ваш заказ успешно оплачен!')
                    }
                }
            }
        }
    });
});