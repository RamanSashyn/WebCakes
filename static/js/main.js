document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('cake-form');
    const totalPriceElement = document.getElementById('total-price');

    const updateTotalPrice = () => {
        let totalPrice = 0;

        form.querySelectorAll('input[type="radio"]:checked, input[type="checkbox"]:checked')
            .forEach(el => {
                const price = Number(el.dataset.price || 0);
                if (!Number.isNaN(price)) totalPrice += price;
            });

        totalPriceElement.textContent = `Итого: ${totalPrice.toLocaleString('ru-RU')}₽`;
    };

    if (form && totalPriceElement) {
        updateTotalPrice();
        form.addEventListener('change', updateTotalPrice);
    }

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
});