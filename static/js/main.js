document.addEventListener('DOMContentLoaded', () => {
    // --- Код для калькулятора цены ---
    const form = document.getElementById('cake-form');
    const totalPriceElement = document.getElementById('total-price');

    // Объявляем функцию updateTotalPrice.
    // Переменная для хранения скидки.
    let currentDiscount = 0;

    const updateTotalPrice = () => {
        let totalPrice = 0;
        if (form) {
            form.querySelectorAll('input[type="radio"]:checked, input[type="checkbox"]:checked')
                .forEach(el => {
                    const price = Number(el.dataset.price || 0);
                    if (!Number.isNaN(price)) totalPrice += price;
                });
        }

        // Применяем скидку к общей цене.
        totalPrice = totalPrice * (1 - currentDiscount / 100);

        if (totalPriceElement) {
            totalPriceElement.textContent = `Итого: ${totalPrice.toLocaleString('ru-RU')}₽`;
        }
    };

    if (form && totalPriceElement) {
        updateTotalPrice();
        form.addEventListener('change', updateTotalPrice);
    }

    // --- Логика для JivoSite ---
    let inactivityTimer;
    const inactivityDuration = 20000;
    let jivoSiteModalShown = false;

    const jivoSiteModalElement = document.getElementById('JivoSiteModal');
    const userInput = document.getElementById('user-input');

    const showJivoSiteModal = () => {
        if (!jivoSiteModalShown && jivoSiteModalElement) {
            const jivoSiteModal = new bootstrap.Modal(jivoSiteModalElement);
            jivoSiteModal.show();
            jivoSiteModalShown = true;
        }
    };

    const resetInactivityTimer = () => {
        clearTimeout(inactivityTimer);
        inactivityTimer = setTimeout(showJivoSiteModal, inactivityDuration);
    };

    document.addEventListener('mousemove', resetInactivityTimer);
    document.addEventListener('keypress', resetInactivityTimer);

    if (form) {
        form.addEventListener('change', resetInactivityTimer);
    }

    resetInactivityTimer();

    if (jivoSiteModalElement) {
        jivoSiteModalElement.addEventListener('shown.bs.modal', () => {
            const startChatButton = document.getElementById('start-chat-button');
            if (startChatButton) {
                startChatButton.addEventListener('click', (event) => {
                    event.preventDefault();

                    const initialMessage = document.getElementById('initial-message');
                    const initialButtons = document.getElementById('initial-buttons');
                    const chatContainer = document.getElementById('chat-container');

                    if (initialMessage) initialMessage.classList.add('d-none');
                    if (initialButtons) initialButtons.classList.add('d-none');
                    if (chatContainer) chatContainer.classList.remove('d-none');

                    setTimeout(() => {
                        addMessage('assistant', "Здравствуйте! Я — ваш помощник. Расскажите, что у вас не получается?");
                    }, 500);

                    if (userInput) {
                        userInput.focus();
                    }
                });
            }
        });
    }

    const addMessage = (sender, text) => {
        const messagesContainer = document.getElementById('messages-container');
        if (messagesContainer) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', sender === 'assistant' ? 'assistant-message' : 'user-message');
            messageElement.textContent = text;
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    };

    if (userInput) {
        userInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter' && userInput.value.trim() !== '') {
                addMessage('user', userInput.value.trim());
                setTimeout(() => {
                    addMessage('assistant', "Я вас понял. Давайте попробуем разобраться вместе");
                }, 600);
                userInput.value = '';
            }
        });
    }

    // --- Логика для промокода ---
    const applyPromoButton = document.getElementById('apply-promo-button');
    const promoCodeInput = document.getElementById('promo-code-input');
    const promoCodeMessage = document.getElementById('promo-code-message');

    if (applyPromoButton) {
        applyPromoButton.addEventListener('click', async () => {
            const promoCode = promoCodeInput.value.trim();
            if (promoCode === '') {
                promoCodeMessage.textContent = 'Введите промокод.';
                promoCodeMessage.style.color = 'red';
                return;
            }

            try {
                const response = await fetch('/api/apply_promo/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf_token
                    },
                    body: JSON.stringify({ code: promoCode })
                });

                const data = await response.json();

                if (data.success) {
                    currentDiscount = parseFloat(data.discount);
                    promoCodeMessage.textContent = `Скидка ${currentDiscount}% применена!`;
                    promoCodeMessage.style.color = 'green';
                } else {
                    currentDiscount = 0;
                    promoCodeMessage.textContent = data.message;
                    promoCodeMessage.style.color = 'red';
                }
            } catch (error) {
                console.error('Ошибка при отправке запроса:', error);
                promoCodeMessage.textContent = 'Произошла ошибка, попробуйте позже.';
                promoCodeMessage.style.color = 'red';
            }
            updateTotalPrice();
        });
    }

});